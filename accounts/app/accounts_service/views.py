import json
from django.db.models import Q

# Create your views here.
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config import *
from paginations import MyPagination
from serializers import *
from django.core.management import call_command

def check_tax_code_of_company(tax_code):
    '''Kiểm tra mã số thuế trước khi thêm mới hoặc chỉnh sửa thông tin account'''
    try:
        response = requests.get(API_GET_INFOR + tax_code)
        data = response.json()
        return data['MaSoThue']
    except Exception as e:
        return None


def check_tax_code(tax_code, account_id):
    '''Kiểm tra mã số thuế trước khi thêm mới hoặc chỉnh sửa thông tin account'''
    try:
        item = accounts.objects.filter(~Q(is_del=1)).filter(tax_code=tax_code).filter(~Q(id=account_id))
        if item.count() > 0:
            return Response({'msg': msg_tax_code_exist,'status':status_already_exists}, status=status.HTTP_400_BAD_REQUEST)
        if tax_code.replace('-', '').isdigit() == False or (len(tax_code) != 10 and len(tax_code) != 14)  or (tax_code.rindex('-') != 10 if '-' in tax_code else '' ):
            return Response({'msg': msg_tax_code_invalid,'status':status_invalid}, status=status.HTTP_400_BAD_REQUEST)
        is_check_web = check_tax_code_of_company(tax_code)
        if is_check_web == None:
            return Response({'msg': msg_tax_code_invalid,'status':status_invalid}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': msg_tax_code_valid,'status':status_valid}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'msg': str(e),'status':status_error}, status=status.HTTP_400_BAD_REQUEST)


def get_queryset(self):
    try:
        data = {}
        info = self.request.query_params
        for key, value in info.items():
            if not value:
                continue
            if key == 'search':
                data['name__contains'] = value
            value = [code for code in value.split(',')]
            if key == 'province':
                data[f'province__code__in'] = value
            if key == 'type':
                data[f'type__title__in'] = value
        # Filter account is displayss
        data['is_del'] = 0
        result = accounts.objects.filter(**data).order_by("-update_date").order_by('-id')
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            return result
    except Exception as e:
        return []


class AccountViewSet(ModelViewSet):
    """Đây là REST API cho Accounts service"""
    queryset = accounts.objects.all()
    serializer_class = AccountSerializers
    pagination_class = MyPagination

    def list(self, request):
        '''Lấy ra tất cả account'''
        queryset = get_queryset(self)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        '''Khi thêm mới 1 account thì đã lựa chọn là cá nhân hay doanh nghiệp rồi'''
        try:
            if 'tax_code' not in request.data or request.data['tax_code'] == None:
                return Response({'msg': msg_required_tax_code_account,'status':status_unsuccessful}, status=status.HTTP_501_NOT_IMPLEMENTED)
            if 'name' not in request.data or request.data['name'] == None:
                return Response({'msg': msg_required_name_account,'status':status_unsuccessful}, status=status.HTTP_501_NOT_IMPLEMENTED)
            is_check_tax_code = check_tax_code(request.data['tax_code'], 0)
            if is_check_tax_code.status_code != 200:
                return Response({'msg': is_check_tax_code.data['msg']}, status=status.HTTP_501_NOT_IMPLEMENTED)
            data_json = convert_data(request.data)
            serializers = AccountCreateSerializers(data=data_json)
            serializers.is_valid()
            serializers.save()
            return Response({'msg': msg_create_success}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''Hiển thi chi tiết account'''
        try:
            account = accounts.objects.filter(pk=pk)
            serializer = AccountSerializers(account, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        '''Chỉnh sửa account '''
        try:
            item_account = accounts.objects.get(pk=pk)
            if 'tax_code' in request.data:
                is_check_tax_code=check_tax_code(request.data['tax_code'], pk)
                if is_check_tax_code.status_code != 200:
                    return Response({'msg': is_check_tax_code.data['msg']}, status=is_check_tax_code.status_code)
            data_json = convert_data(request.data)
            data_json['update_date'] = Timer.get_timestamp_now()
            serializers = AccountCreateSerializers(instance=item_account,data=data_json)
            serializers.is_valid()
            serializers.save()
            # for key, value in data_json.items():
            #   setattr(item_account, key, value)
            # item_account.save()
            return Response({'msg': msg_edit_success}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, user_id=None):
        '''Xóa thông tin account: không ai được phép xóa ngoại trừ GĐ doanh nghiệp (role = 0)'''
        try:
            response = requests.get(API_USER_DETAIL + str(user_id))
            geodata = response.json()
            role = geodata['level_detail']['level']
            if role != 0:  # Là GĐ mới có quyền xóa
                return Response({'msg': msg_not_permission_delete_account},status=status.HTTP_403_FORBIDDEN)
            account = accounts.objects.get(pk=pk)
            account.is_del = 1
            account.save()
            return Response({'msg': msg_delete_customer + str(account.name)},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def check_tax_code_api(self, request):
        '''Kiểm tra mã số thuế trước khi thêm mới hoặc chỉnh sửa thông tin account'''
        try:
            is_check = check_tax_code(request.query_params['tax_code'], 0)
            return Response({'msg': is_check.data['msg']}, status=is_check.status_code)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_information_company(self, request):
        try:
            response = requests.get(API_GET_INFOR+request.query_params['tax_code'])
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def list_all_element(self, request):
        '''Lấy ra tất cả list elements'''
        try:
            datas = []
            data = employees.objects.all()
            serializer = ListElementAllSerializers(data, many=True)
            datas.append({'elements':serializer.data})
            data = fields.objects.all()
            serializer = FieldsSerializers(data, many=True)
            datas.append({'fields': serializer.data})
            data = potentials.objects.all()
            serializer = PotentialsSerializers(data, many=True)
            datas.append({'potentials': serializer.data})
            data = capital_investments.objects.all()
            serializer = Capital_investmentsSerializers(data, many=True)
            datas.append({'investments': serializer.data})
            data = level_accounts.objects.all()
            serializer = Type_accountsSerializers(data, many=True)
            datas.append({'level': serializer.data})
            data = type_company.objects.all()
            serializer = Type_companysSerializers(data, many=True)
            datas.append({'company': serializer.data})
            if 'type' in request.query_params:
                if request.query_params['type'] == 'employees':
                    data = employees.objects.all()
                    serializer = NumberEmployeesSerializers(data, many=True)
                if request.query_params['type'] == 'fields':
                    data = fields.objects.all()
                    serializer = FieldsSerializers(data, many=True)
                if request.query_params['type'] == 'potentials':
                    data = potentials.objects.all()
                    serializer = PotentialsSerializers(data, many=True)
                if request.query_params['type'] == 'investments':
                    data = capital_investments.objects.all()
                    serializer = Capital_investmentsSerializers(data, many=True)
                if request.query_params['type'] == 'level':
                    data = level_accounts.objects.all()
                    serializer = Type_accountsSerializers(data, many=True)
                if request.query_params['type'] == 'company':
                    data = type_company.objects.all()
                    serializer = Type_companysSerializers(data, many=True)
                if request.query_params['type'] == 'countrys':
                    data = countrys.objects.all()
                    serializer = CountrysSerializers(data, many=True)
                if request.query_params['type'] == 'provinces':
                    data = provinces.objects.all()
                    serializer = ProvincesSerializers(data, many=True)
                if request.query_params['type'] == 'wards':
                    data = wards.objects.all()
                    serializer = WardsSerializers(data, many=True)
                if request.query_params['type'] == 'districts':
                    data = districts.objects.all()
                    serializer = DistrictsSerializers(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(datas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def list_all_element_address(self, request):
        '''Lấy ra tất cả list elements'''
        try:
            datas = []
            data = countrys.objects.all()
            serializer = CountrysSerializers(data, many=True)
            datas.append({'countrys': serializer.data})
            data = provinces.objects.all()
            serializer = ProvincesSerializers(data, many=True)
            datas.append({'provinces': serializer.data})
            data = wards.objects.all()
            serializer = WardsSerializers(data, many=True)
            datas.append({'wards': serializer.data})
            data = districts.objects.all()
            serializer = DistrictsSerializers(data, many=True)
            datas.append({'districts': serializer.data})
            return Response(datas, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def load_data_first(self,request):
        try:
            call_command('loaddata', 'initial_data.json',verbosity=0)
        except Exception as e:
            return Response({'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'Thành công!','status':status_successful}, status=status.HTTP_200_OK)
