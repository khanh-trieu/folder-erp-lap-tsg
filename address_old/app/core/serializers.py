from rest_framework import serializers

from core.models import *


class CountrysSerializers(serializers.ModelSerializer):

    # currencies = serializers.SerializerMethodField('get_currencies')
    #
    # def get_currencies(self,country):
    #     data = []
    #     for ele in currencies.objects.filter(pk__in=country.currencies):
    #         param = {
    #             'code': ele.code,
    #             'name': ele.name
    #         }
    #         data.append(param)
    #     return data

    class Meta:
        model = countrys
        fields = '__all__'

class ProvinceSerializers(serializers.ModelSerializer):

    country = serializers.SerializerMethodField('get_country')

    def get_country(self,province):
        return province.country.name

    class Meta:
        model = provinces
        fields = '__all__'

class DistrictsSerializers(serializers.ModelSerializer):

    province = serializers.SerializerMethodField('get_province')

    def get_province(self, district):
        return district.province.name

    class Meta:
        model = districts
        fields = '__all__'


class WardsSerializers(serializers.ModelSerializer):
    dictrict = serializers.SerializerMethodField('get_province')

    def get_province(self, ward):
        return ward.district.name

    class Meta:
        model = wards
        fields = '__all__'


class CreateCountrysSerializers(serializers.ModelSerializer):

    class Meta:
        model = countrys
        fields = '__all__'

class CreateProvinceSerializers(serializers.ModelSerializer):

    class Meta:
        model = provinces
        fields = '__all__'

class CreateDistrictsSerializers(serializers.ModelSerializer):

    class Meta:
        model = districts
        fields = '__all__'


class CreateWardsSerializers(serializers.ModelSerializer):

    class Meta:
        model = wards
        fields = '__all__'