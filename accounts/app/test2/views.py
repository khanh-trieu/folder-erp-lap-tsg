# -*- coding: utf-8 -*-
import threading

from django.shortcuts import render

# Create your views here.
import json
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config import *
from paginations import MyPagination
from serializers import *


class TestViewSet(ModelViewSet):
    """Đây là REST API cho Accounts service"""
    queryset = accounts.objects.all()
    serializer_class = AccountSerializers
    pagination_class = MyPagination

    def list(self, request):
        '''Lấy ra tất cả account'''
        data = []
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        '''Khi thêm mới 1 account thì đã lựa chọn là cá nhân hay doanh nghiệp rồi'''
        try:

            for i in [4,5,6,7,8,9,10]:
                # with open('D:\\\company_split\\company.s02', encoding='utf-8') as json_file:
                with open('D:\\company_split\\company.s0'+str(i)+'.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    type = type_company.objects.get(title='enterprise')
                    for item in data:
                        try:
                            mst = accounts.objects.filter(tax_code=item['MaSoThue'])
                            if not mst:
                                bb = accounts.objects.create(
                                    name=item['Title'],
                                    en_name=item['TitleEn'],
                                    tax_code=item['MaSoThue'],
                                    representer=item['ChuSoHuu'],
                                    tax_date_start=item['NgayCap'],
                                    tax_date_close=item['NgayDongMST'],
                                    address=item['DiaChiCongTy'],
                                    type=type,
                                    email_provider='',
                                    country=countrys.create_or_no_update('Việt Nam', 'VN'),
                                    province=provinces.create_or_no_update(item['TinhThanhTitle'], item['TinhThanhID']),
                                    district=districts.create_or_no_update(item['QuanHuyenTitle'], item['QuanHuyenID']),
                                    ward=wards.create_or_no_update(item['PhuongXaTitle'], item['PhuongXaID']),
                                    emails='',
                                    phones=''
                                )
                                print(bb.name)
                        except Exception as e:
                            continue
            #
            # data_json = convert_data(request.data)
            # serializers = AccountCreateSerializers(data=data_json)
            # serializers.is_valid()
            # serializers.save()
            return Response({'msg': msg_create_success}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def update(self, request, pk=None):
        '''Chỉnh sửa account '''
        try:
            acc_all = accounts.objects.filter(fields=None)
            for item in acc_all:
                response = requests.get('https://thongtindoanhnghiep.co/api/company/'+item.tax_code)
                item.fields = response.json()['NganhNgheID']
                item.save()
                print(item.name)
            return Response({'msg': msg_edit_success}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)


    def crawl_filed(self,request):
        try:
            response = requests.get('https://thongtindoanhnghiep.co/api/industry')
            if response.json()['LtsItem']:
                for data in response.json()['LtsItem']:
                    try:
                        if fields.objects.filter(code=data['ID']):
                            continue
                        data['title'] = data['Title']
                        data['code'] = data['ID']
                        serializer = FieldsSerializers(data=data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        print(data['Title'])
                    except Exception as e:
                        print(e)
                        continue
            return Response({'msg': msg_edit_success}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def update_code_address(self,request):
        try:
            lts_province = provinces.objects.all()
            for i_p in lts_province:
                lts = accounts.objects.filter(province_id=i_p.id)
                for i in lts:
                    try:
                        i.province_code = i.province.code
                        i.country_code = 'VN'
                        i.district_code = i.district.code
                        i.ward_code = i.ward.code
                        i.save()
                        print(i.name)
                    except Exception as e:
                        continue
            return Response({'msg': msg_edit_success}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_501_NOT_IMPLEMENTED)
