from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from app.config import *
from app.core.serializers import *

# Create your views here.
from app.core.models import *


class ProvincesViewSet(viewsets.ViewSet):
    def list(self, request):
        province = provinces.objects.all()

        serializer = ProvinceSerializers(province, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        response = requests.get(API_GET_PROVINCE)
        if 'country_code' in request.data:
            for data in response.json()['results']:
                try:
                    if provinces.objects.filter(code=data['code']):
                        continue
                    data['country'] = countrys.objects.get(code=request.data['country_code']).id
                    serializer = CreateProvinceSerializers(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    response_districts = requests.get(API_GET_DISTRICT+data['code'])
                    for district in response_districts.json()['results']:
                        if districts.objects.filter(code=data['code']):
                            continue
                        district['province'] = provinces.objects.get(code=data['code']).id
                        serializer = CreateDistrictsSerializers(data=district)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        response_wards = requests.get(API_GET_WARD + district['code'])
                        for ward in response_wards.json()['results']:
                            if wards.objects.filter(code=data['code']):
                                continue
                            ward['district'] = districts.objects.get(code=district['code']).id
                            serializer = CreateWardsSerializers(data=ward)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                    print(data['name'])
                except Exception as e:
                    print(e)
                    continue
        return Response({'message':MSG_SUCCESS}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        province = provinces.objects.get(pk=pk)
        serializer = ProvinceSerializers(data=province)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        province = provinces.objects.get(pk=pk)
        serializer = ProvinceSerializers(instance=province, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        province = provinces.objects.get(pk=pk)
        province.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistrictViewSet(viewsets.ViewSet):

    def list(self, request):
        data = districts.objects.all()
        if 'province_code' in request.query_params:
            data = data.filter(province__code=request.query_params['province_code'])
        serializer = DistrictsSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        data = districts.objects.filter(pk=pk)
        serializer = DistrictsSerializers(data, many=True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)


class WardsViewSet(viewsets.ViewSet):

    def list(self, request):
        data = wards.objects.all()
        if 'district_code' in request.query_params:
            data = data.filter(district__code=request.query_params['district_code'])
        serializer = WardsSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        data = wards.objects.filter(pk=pk)
        serializer = WardsSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

