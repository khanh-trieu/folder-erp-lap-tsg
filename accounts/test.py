import json
import threading

import psycopg2

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
    item['TitleEn'] = item['TitleEn'] if item['TitleEn'] != None else "' '"
    insert_query = "INSERT INTO core_accounts (name, en_name, tax_code, representer, tax_date_start, tax_date_close, type_id, email_provider, country_id, province_id, district_id, ward_id, emails,phones,is_del,created_date,update_date,address,fields)  VALUES ( N'" + \
                   item['Title'].replace("'","") + "', '', '" + item['MaSoThue'] + "','" + item['ChuSoHuu'] + "','" + item[
                       'NgayCap'] + "',null,2,'',1," + str(id_province) + "," + str(id_district) + "," + str(
        id_ward) + ",'','',0,1618808371,1618808371,'" + item['DiaChiCongTy'].replace("'","") + "',"+str(item['NganhNgheID'])+")"
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
    connection = connects()

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    # Print PostgreSQL details
    for i in list(range(30, 51)):
        with open('D:\\company_split\\company.s'+str(i)+'.json', encoding='utf-8') as reader:
            # lines = reader.readlines()
            # print(len(lines))
            data = json.load(reader)

            i = 0
            for item in data:
                cursor.execute("SELECT * FROM core_accounts where tax_code = '" + item['MaSoThue'] + "'")
                record = cursor.fetchall()
                # print(record)
                # break
                if record == []:
                    try:
                        thread = WorkerThread(item)
                        thread.start()
                        thread.join()
                    except Exception as e:
                        print(str(e))
                        continue


db_connect()

