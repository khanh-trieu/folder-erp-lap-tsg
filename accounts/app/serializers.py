import sys

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import Field, CharField

from app_common import Convert_timestamp
from core.models import *


def get_phone_type(self):
    type = phone_type.objects.filter(id=self.phone_type.id).first()
    return type

def set_country(code):
    item = countrys.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_province(code):
    item = provinces.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_district(code):
    item = districts.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_ward(code):
    item = wards.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_employee(code):
    item = employees.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_company(code):
    item = type_company.objects.filter(title=code)
    if item:
        id = item.first().id
    return id

def set_potential(code):
    item = potentials.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_level(code):
    item = level_accounts.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def set_investment(code):
    item = capital_investments.objects.filter(code=code)
    if item:
        id = item.first().id
    return id

def convert_data(data_json):
    if 'emails' in data_json and data_json['emails']:
        data_json['emails'] = ','.join(data_json['emails'])
    if 'fields' in data_json and data_json['fields']:
        data_json['fields'] = ','.join(data_json['fields'])
    if 'phones' in data_json and data_json['phones']:
        data_json['phones'] = ','.join(data_json['phones'])
    if 'contacts' in data_json and data_json['contacts']:
        data_json['contacts'] = ','.join([str(int) for int in data_json['contacts']])
    if 'country' in data_json and data_json['country']:
        data_json['country'] = set_country(data_json['country'])
    if 'province' in data_json and data_json['province']:
        data_json['province'] = set_province(data_json['province'])
    if 'district' in data_json and data_json['district']:
        data_json['district'] = set_district(data_json['district'])
    if 'ward' in data_json and data_json['ward']:
        data_json['ward'] = set_ward(data_json['ward'])
    if 'employee' in data_json and data_json['employee']:
        data_json['employee'] = set_employee(data_json['employee'])
    if 'potential' in data_json and data_json['potential']:
        data_json['potential'] = set_potential(data_json['potential'])
    if 'level' in data_json and data_json['level']:
        data_json['level'] = set_level(data_json['level'])
    if 'investment' in data_json and data_json['investment']:
        data_json['investment'] = set_investment(data_json['investment'])
    if 'company' in data_json and data_json['company']:
        data_json['type'] = set_company(data_json['company'])
    return data_json

class AccountSerializers(serializers.ModelSerializer):
    ''''''
    created_date = serializers.SerializerMethodField('get_created_date')
    update_date = serializers.SerializerMethodField('get_update_date')
    emails = serializers.SerializerMethodField('get_list_email')
    phones = serializers.SerializerMethodField('get_list_phone')
    country = serializers.SerializerMethodField('get_country')
    province = serializers.SerializerMethodField('get_province')
    fields = serializers.SerializerMethodField('get_field')
    employee = serializers.SerializerMethodField('get_number_employees')
    company = serializers.SerializerMethodField('get_type_company')
    level = serializers.SerializerMethodField('get_level')
    potential = serializers.SerializerMethodField('get_potential')
    investment = serializers.SerializerMethodField('get_capital_investment')
    ward = serializers.SerializerMethodField('get_ward')
    district = serializers.SerializerMethodField('get_district')
    contacts = serializers.SerializerMethodField('get_contact')

    def get_contact(self, accounts):
        try:
            result = accounts.contacts.split(",")
            return result
        except Exception as e:
            return []

    def get_capital_investment(self,accounts):
        try:
            param = {
                     'key': accounts.investment.code,
                     'value':accounts.investment.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_ward(self,accounts):
        try:
            param = {
                     'key': accounts.ward.code,
                     'value':accounts.ward.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_district(self,accounts):
        try:
            param = {
                     'key': accounts.district.code,
                     'value':accounts.district.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_level(self,accounts):
        try:
            param = {
                     'key': accounts.level.code,
                     'value': accounts.level.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_potential(self,accounts):
        try:
            param = {
                     'key': accounts.potential.code,
                     'value':accounts.potential.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_type_company(self,accounts):
        try:
            param = {
                'key': accounts.type.type[0][0] if accounts.type.type[0][0] == accounts.type.title else accounts.type.type[1][0],
                'value': accounts.type.type[0][1] if accounts.type.type[0][0] == accounts.type.title else accounts.type.type[1][1],
            }
            return param
        except Exception as e:
            print(e)
            return []

    def get_field(self,accounts):
        data = []
        try:
            for ele in fields.objects.filter(code__in=accounts.fields.split(',')):
                param = {
                         'key': ele.code,
                         'value': ele.title
                         }
                data.append(param)
            return data
        except Exception as e:
            return data

    def get_number_employees(self,accounts):
        try:
            param = {
                     'key': accounts.employee.code,
                     'value':accounts.employee.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_country(self,accounts):
        try:
            param = {
                     'key': accounts.country.code,
                     'value':accounts.country.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_province(self,accounts):
        try:
            param = {
                     'key': accounts.province.code,
                     'value': accounts.province.title
                     }
            return param
        except Exception as e:
            print(e)
            return []

    def get_created_date(self, accounts):
        return Convert_timestamp(accounts.created_date)

    def get_update_date(self, accounts):
        return Convert_timestamp(accounts.update_date)

    def get_list_phone(self, accounts):
        data = []
        try:
            for ele in accounts.phones.split(','):
                data.append(ele)
            return data
        except Exception as e:
            return data

    def get_list_email(self, accounts):
        data = []
        try:
            for ele in accounts.emails.split(','):
                data.append(ele)
            return data
        except Exception as e:
            return data

    class Meta:
        model = accounts
        fields = '__all__'



class ListElementAllSerializers(serializers.ModelSerializer):


    class Meta:
        model = employees
        fields = '__all__'


class AccountCreateSerializers(serializers.ModelSerializer):

    class Meta:
        model = accounts
        fields = '__all__'


class NumberEmployeesSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = employees
        fields = '__all__'


class FieldsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = fields
        fields = '__all__'


class PotentialsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = potentials
        fields = '__all__'


class Capital_investmentsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = capital_investments
        fields = '__all__'


class Type_accountsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = level_accounts
        fields = '__all__'


class Type_companysSerializers(serializers.ModelSerializer):
    ''''''
    company = serializers.SerializerMethodField('get_type_company')

    def get_type_company(self,accounts):
        try:
            return accounts.type[0][1] if accounts.type[0][0] == accounts.title else accounts.type[1][1]
        except Exception as e:
            print(e)
            return []

    class Meta:
        model = type_company
        fields = '__all__'


class CountrysSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = countrys
        fields = '__all__'


class ProvincesSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = provinces
        fields = '__all__'


class Phone_typeSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = phone_type
        fields = '__all__'


class WardsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = wards
        fields = '__all__'


class DistrictsSerializers(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = districts
        fields = '__all__'
