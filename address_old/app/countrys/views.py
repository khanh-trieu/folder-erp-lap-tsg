from django.shortcuts import render
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from core.models import *
from core.serializers import CountrysSerializers


class CountsViewSet(viewsets.ViewSet):
    def list(self, request):
        country = countrys.objects.all()
        serializer = CountrysSerializers(country, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        response = requests.get('https://restcountries.eu/rest/v2/all')
        response.json()
        for data in response.json():
            try:
                ite = countrys.objects.filter(code= data['alpha2Code'])
                if ite:
                    continue
                data['code'] = data['alpha2Code']
                data['callingCodes'] = ','.join(data['callingCodes'])
                data['timezones'] = ','.join(data['timezones'])
                data['currencies'] = currencies.create_or_no_update(data['currencies'])
                data['languages'] = languages.create_or_no_update(data['languages'])

                serializer = CountrysSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                print(data['code'])
            except Exception as e:
                print(e)
                continue
        return Response({'massage':'Thành công!'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        country = countrys.objects.get(pk=pk)
        serializer = CountrysSerializers(data=country)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        country = countrys.objects.get(pk=pk)
        serializer = CountrysSerializers(instance=country, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        country = countrys.objects.get(pk=pk)
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

