import json
from datetime import datetime
import requests
import scrapy.crawler as crawler
from twisted.internet import reactor
import scrapy
from azure.storage.blob import BlobServiceClient
import json
import threading
import psycopg2
# from airflow.models import Variable



root_domain = 'https://thongtindoanhnghiep.co'
api = 'https://thongtindoanhnghiep.co/api/company/'
city_api = 'https://thongtindoanhnghiep.co/api/city'
data_city_api = 'https://thongtindoanhnghiep.co/tinh-thanh-pho'
data_new_day_api = 'https://thongtindoanhnghiep.co'


# path_file_json='/home/ubuntu/erp-accounts/company_01.json'
path_file_json='D:\\ERP\\'
name_file_json = 'company-'+ str(datetime.now().date()) + '.json'
connect_string = 'DefaultEndpointsProtocol=https;AccountName=datacompanycrawltoapi;AccountKey=kcYD28Pe/kl0UH+zfcL5V3LU+p3vf9GByVxhhwU2TiI0q/bHUBIYu3zatU/Qb2DI5NV86zMv8CqanfswJstxlA==;EndpointSuffix=core.windows.net'
container_name = 'company2021'


def connects():
    connection = psycopg2.connect(user="postgresadmin",
                                  password="postgrespwd",
                                  host="20.44.210.149",
                                  port="5433",
                                  database="postgresdb")
    return  connection
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
        cursor.execute("SELECT id FROM " + name_table + " where title = '" + title.replace("'","") + "' ")
        record = cursor.fetchall()
    return record[0][0]

def insert(item):
    connection = connects()
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    id_province = create_or_no_update('core_provinces', item['TinhThanhTitle'], item['TinhThanhID'])
    id_district = create_or_no_update('core_districts', item['QuanHuyenTitle'], item['QuanHuyenID'])
    id_ward = create_or_no_update('core_wards', item['PhuongXaTitle'], item['PhuongXaID'])
    date_time_stamp = int(datetime.today().timestamp())
    item['NganhNgheID'] = str(item['NganhNgheID']) if item['NganhNgheID'] != None else "' '"
    item['TitleEn'] = item['TitleEn'] if item['TitleEn'] != None else "' '"
    insert_query = "INSERT INTO core_accounts (name, en_name, tax_code, representer, tax_date_start, tax_date_close, type_id, email_provider, country_id, province_id, district_id, ward_id, emails,phones,is_del,created_date,update_date,address,fields)  VALUES ( N'" + \
                   item['Title'].replace("'","") + "', '', '" + item['MaSoThue'] + "','" + item['ChuSoHuu'] + "','" + item[
                       'NgayCap'] + "',null,2,'',1," + str(id_province) + "," + str(id_district) + "," + str(
        id_ward) + ",'','',0,"+str(date_time_stamp)+","+str(date_time_stamp)+",'" + item['DiaChiCongTy'].replace("'","") + "',"+item['NganhNgheID']+")"
    cursor.execute(insert_query)
    connection.commit()
    print(item['Title'])

class WorkerThread(threading.Thread):
    def __init__(self,item):
        super().__init__()
        self.item = item

    def run(self) -> None:
        insert(self.item)

def db_connect():
    try:
        connection = connects()

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Print PostgreSQL details

        with open(path_file_json+name_file_json, encoding='utf-8') as reader:
            # lines = reader.readlines()
            # print(len(lines))
            data = json.load(reader)
            for item in data:
                cursor.execute("SELECT * FROM core_accounts where tax_code = '" + item['MaSoThue'] + "'")
                record = cursor.fetchall()
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

def upload_file_to_blob():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connect_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=name_file_json)
        with open(path_file_json+name_file_json, "rb") as data:
            blob_client.upload_blob(data, blob_type="BlockBlob", length=None, metadata=None, overwrite=True)
        print('Update file json success!')
    except Exception as e:
        print(str(e))

datas = []
class MySpider(scrapy.Spider):
    name = 'spider'

    def start_requests(self):
        crawl_url = f'{data_new_day_api}'
        yield scrapy.Request(url=crawl_url, callback=self.parse_page)

    def parse_page(self, response):
        company_item = response.css('div.news-v3 .row')

        for item in company_item:
            try:
                mst = item.css('div h3 strong a::text').get()
                day_create = item.css('div p::text')[1].get()
                day_create = day_create.split(' ')[len(day_create.split(' '))-1].replace('-','/')
                day_create = datetime.strptime(day_create, '%d/%m/%Y')
                # if day_create.date() >= datetime.now().date():
                #     return
                response_company = requests.get(api+mst)
                datas.append(response_company.json())

            except Exception as e:
                continue
        next = response.xpath("//ul[@class='pagination']//a[contains(text(), 'Sau')]").xpath('@href').get()
        if next:
            next_url = f'{root_domain}{next}'
            yield scrapy.Request(next_url, callback=self.parse_page)
        if datas:
            with open(path_file_json + name_file_json, 'a') as outfile:
                json.dump(datas, outfile)
            upload_file_to_blob()
            db_connect()

def run_spider(spider):
    try:
        runner = crawler.CrawlerRunner(
            settings={
                "FEEDS": {
                   path_file_json+name_file_json: {"format": "json"},
                },
                "CONCURRENT_REQUESTS": 50,
                "CONCURRENT_ITEMS": 50,
                "FEED_EXPORT_ENCODING": 'utf-8',
                "LOG_ENABLED": False,
                # 'ITEM_PIPELINES': ['MongoDBPipeline']
              })
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        print("Success!")
    except Exception as e:
        print(str(e))

run_spider(MySpider)

