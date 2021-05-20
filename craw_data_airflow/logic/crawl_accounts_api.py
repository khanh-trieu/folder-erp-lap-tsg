import os
from datetime import datetime
from pathlib import Path
from os import path
import requests
import scrapy.crawler as crawler
from twisted.internet import reactor
import scrapy
from azure.storage.blob import BlobServiceClient
import json
import threading
import psycopg2
from airflow.models import Variable
root_domain = 'https://thongtindoanhnghiep.co'
api = 'https://thongtindoanhnghiep.co/api/company/'
city_api = 'https://thongtindoanhnghiep.co/api/city'
data_city_api = 'https://thongtindoanhnghiep.co/tinh-thanh-pho'
data_new_day_api = 'https://thongtindoanhnghiep.co'
name_file_json ='company-'+ str(datetime.now().date()) + '.json'
path_file_json = Variable.get("path_file_json")
connect_string = Variable.get("connect_string")
container_name = Variable.get("name_container")
# name_file_json = 'company-'+ str(datetime.now().date()) + '.json'
# path_file_json ='\\ERP\\erp-airflow-crwal-accounts\\logic\\'
# connect_string='DefaultEndpointsProtocol=https;AccountName=datacompanycrawltoapi;AccountKey=kcYD28Pe/kl0UH+zfcL5V3LU+p3vf9GByVxhhwU2TiI0q/bHUBIYu3zatU/Qb2DI5NV86zMv8CqanfswJstxlA==;EndpointSuffix=core.windows.net'
# container_name = 'company2021'

show_list_tax_code = []


def connects():
    connection = psycopg2.connect(user="postgresadmin",
                                  password="postgrespwd",
                                  host="20.44.210.149",
                                  port="5433",
                                  database="postgresdb")
    return connection


def create_or_no_update(name_table,title,code):
    connection = connects()
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    cursor.execute("SELECT id FROM "+name_table+" where title = N'"+title.replace("'","")+"'")
    record = cursor.fetchall()
    if record == []:
        insert_query =  "INSERT INTO "+name_table+" (title, code) VALUES ('"+title.replace("'","")+"','"+str(code)+"')"
        cursor.execute(insert_query)
        connection.commit()
        cursor.execute("SELECT id FROM " + name_table + " where title = '" + title.replace("'", "") + "' ")
        record = cursor.fetchall()
    return record[0][0]


def insert(item):
    connection = connects()
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    id_province = create_or_no_update('core_provinces', item['TinhThanhTitle'], item['TinhThanhID'])
    id_district = create_or_no_update('core_districts', item['QuanHuyenTitle'], item['QuanHuyenID'])
    id_ward = create_or_no_update('core_wards', item['PhuongXaTitle'], item['PhuongXaID'])
    code_province = str(item['TinhThanhID'])
    code_district =  str(item['QuanHuyenID'])
    code_ward = str(item['PhuongXaID'])
    date_time_stamp = int(datetime.today().timestamp())
    item['NganhNgheID'] = str(item['NganhNgheID']) if item['NganhNgheID'] != None else "' '"
    item['TitleEn'] = item['TitleEn'] if item['TitleEn'] != None else "' '"
    insert_query = "INSERT INTO core_accounts (name, en_name, tax_code, representer, tax_date_start, tax_date_close, type_id," \
                   " email_provider, country_id, province_id, district_id, ward_id, emails,phones,is_del,created_date,update_date,address,fields,country_code,province_code,district_code,ward_code)  VALUES ( N'" + \
                   item['Title'].replace("'", "") + "', '', '" + item['MaSoThue'] + "','" + item['ChuSoHuu'] + "','" + \
                   item['NgayCap'] + "',null,2,'',1," + str(id_province) + "," + str(id_district) + "," + str(id_ward) +\
                   ",'','',0," + str(date_time_stamp) + "," + str(date_time_stamp) + ",'" + item['DiaChiCongTy'].replace("'", "") + \
                   "'," + item['NganhNgheID'] + ",'VN',"+str(code_province)+","+str(code_district)+","+str(code_ward)+")"
    cursor.execute(insert_query)
    connection.commit()


class WorkerThread(threading.Thread):
    def __init__(self,item):
        super().__init__()
        self.item = item

    def run(self) -> None:
        insert(self.item)


def db_connect():
    try:
        connection = connects()
        cursor = connection.cursor()
        with open(path_file_json+name_file_json) as reader:
            print(str(path_file_json)+str(name_file_json))
            data = json.load(reader)
            print(data)
            for item in data:
                print(item)
                cursor.execute("SELECT * FROM core_accounts where tax_code = '" + item['MaSoThue'] + "'")
                record = cursor.fetchall()
                print(record)
                if record == []:
                    try:
                        thread = WorkerThread(item)
                        thread.start()
                        thread.join()
                    except Exception as e:
                        print(str(e))
                        continue
    except Exception as e:
        print(str(e))


def upload_file_to_blob(path_file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=name_file_json)
        print(path_file)
        with open(path_file, "rb") as data:
            blob_client.upload_blob(data, blob_type="BlockBlob", length=None, metadata=None, overwrite=True)
        print('Update file json success!')
    except Exception as e:
        print(str(e))


def check_size_file():
    try:
        if path.isfile(path_file_json + name_file_json):
            f = open(path_file_json + name_file_json, "r+")
            f.seek(0)
            f.truncate()
        return True
    except Exception as e:
        print(str(e))
        return False


class MySpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        crawl_url = f'{data_new_day_api}'
        yield scrapy.Request(url=crawl_url, callback=self.parse_page)

    def parse_page(self, response):
        company_item = response.css('div.news-v3 .row')
        check_size_file()
        for item in company_item:
            try:
                mst = item.css('div h3 strong a::text').get()
                # day_create = item.css('div p::text')[1].get()
                # day_create = day_create.split(' ')[len(day_create.split(' ')) - 1].replace('-', '/')
                # day_create = datetime.strptime(day_create, '%d/%m/%Y')
                # if day_create.date() < datetime.now().date():
                #     continue
                response_company = requests.get(api + mst)
                show_list_tax_code.append(mst)
                yield response_company.json()
            except Exception as e:
                continue
        next = response.xpath("//ul[@class='pagination']//a[contains(text(), 'Sau')]").xpath('@href').get()
        if next:
            next_url = f'{root_domain}{next}'
            yield scrapy.Request(next_url, callback=self.parse_page)
        yield ']'


def run_spider(spider):
    try:
        f = open(name_file_json, "w")
        path_file = os.path.abspath(name_file_json)
        print(path_file)
        runner = crawler.CrawlerRunner(
              settings={
                "FEEDS": {
                    name_file_json: {"format": "json"},
                },
                "CONCURRENT_REQUESTS": 50,
                "CONCURRENT_ITEMS": 50,
                "LOG_ENABLED": False,
                # 'ITEM_PIPELINES': ['MongoDBPipeline']
              }
            )
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        if len(show_list_tax_code) > 0:
            upload_file_to_blob(path_file)
            # db_connect()
            print(show_list_tax_code)
        print("Success!")
    except Exception as e:
        print(str(e))


run_spider(MySpider)








