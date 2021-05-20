

from django.db import models

# Create your models here.
from app_common import Timer



class employees(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title + ' - ' + self.code


class fields(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title + ' - ' + self.code


class provinces(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self,code):
        item_type = provinces.objects.filter(title=self)
        if item_type.count() == 0:
            item_phone_type = provinces.objects.create(title=self, code=code)
            return item_phone_type
        return item_type.first()

    def __str__(self):
        return self.title + ' - ' + self.code


class districts(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self,code):
        item_type = districts.objects.filter(title=self)
        if item_type.count() == 0:
            item_phone_type = districts.objects.create(title=self, code=code)
            return item_phone_type
        return item_type.first()

    def __str__(self):
        return self.title + ' - ' + self.code


class wards(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self,code):
        item_type = wards.objects.filter(title=self)
        if item_type.count() == 0:
            item_phone_type = wards.objects.create(title=self, code=code)
            return item_phone_type
        return item_type.first()

    def __str__(self):
        return self.title + ' - ' + self.code


class countrys(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self,code):
        item_type = countrys.objects.filter(title=self)
        if item_type.count() == 0:
            item_phone_type = countrys.objects.create(title=self, code=code)
            return item_phone_type
        return item_type.first()

    def __str__(self):
        return self.title + ' - ' + self.code


class phone_type(models.Model):
    code = models.CharField(max_length=250, blank=True,null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        item_type = phone_type.objects.filter(code = self)
        if item_type.count() == 0:
            item_phone_type = phone_type.objects.create(title=self,code=self)
            return item_phone_type
        return item_type.first()

    def __str__(self):
        return self.title + ' - ' + self.code


class account_channel_phones(models.Model):
    '''Loại số điện thoại'''
    phone_type = models.ForeignKey(phone_type,on_delete=models.CASCADE,default=None,blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.phone_number + '_' + str(self.phone_type)


class account_channel_emails(models.Model):
    email = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        item_type = account_channel_emails.objects.filter(email = self)
        if item_type.count() == 0:
            new_email= account_channel_emails.objects.create(email=self)
            return new_email
        return item_type.first()

    def __str__(self):
        return self.email

class type_company(models.Model):
    personal='personal'
    enterprise ='enterprise'
    type = (
        (personal,'Cá nhân'),
        (enterprise,'Doanh nghiệp')
    )
    title = models.CharField(choices=type,max_length=100,null=True)

    def create_or_no_update(self):
        item_type = type_company.objects.filter(title = self)
        if item_type.count() == 0:
            type = type_company.objects.create(title=self)
            return type
        return item_type.first()

    def __str__(self):
        return self.title


class level_accounts(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        try:
            item_type = level_accounts.objects.filter(title = self)
            if item_type.count() == 0:
                level_accounts.objects.create(title=self)
            return True
        except Exception as e:
            print(e)
            return False
    def __str__(self):
        return self.title + ' - ' + self.code


class capital_investments(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        try:
            item_type = capital_investments.objects.filter(title = self)
            if item_type.count() == 0:
                capital_investments.objects.create(title=self)
            return True
        except Exception as e:
            print(e)
            return False
    def __str__(self):
        return self.title + ' - ' + self.code


class potentials(models.Model):
    code = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        try:
            item_type = potentials.objects.filter(title = self)
            if item_type.count() == 0:
                potentials.objects.create(title=self)
            return True
        except Exception as e:
            print(e)
            return False
    def __str__(self):
        return self.title + ' - ' + self.code


class accounts(models.Model):
    '''Tên account'''
    name = models.CharField(max_length=250, null=False)
    '''Tên tiếng anh của account'''
    en_name = models.CharField(max_length=250, blank=True)
    '''Mã số thuế'''
    tax_code = models.CharField(max_length=100,null=False)
    '''representer: người đại diện pháp luật'''
    representer = models.CharField(max_length=100, blank=True, null=True)
    '''Ngày được cấp mã số thuế'''
    tax_date_start = models.CharField(max_length=100, blank=True,null=True)
    '''Ngày thu hồi mã số thuế'''
    tax_date_close = models.CharField(max_length=100, blank=True,null=True)
    '''address: địa chỉ tiếng việt'''
    address = models.CharField(max_length=250, blank=True, null=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    email_provider = models.CharField(max_length=250, null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)
    number_of_pc = models.IntegerField(null=True, blank=True)
    number_of_server = models.IntegerField(null=True, blank=True)
    '''user id tạo account '''
    user_id = models.IntegerField(null=True)
    ''' account được user chăm sóc'''
    supporter_id = models.IntegerField(null=True)
    """contact_id"""
    contacts = models.CharField(max_length=250, null=True, blank=True)
    '''quốc gia'''
    country = models.ForeignKey(countrys, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''mã quốc gia'''
    country_code = models.CharField(max_length=250, null=True, blank=True)
    '''tỉnh thành'''
    province = models.ForeignKey(provinces, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''mã tỉnh thành'''
    province_code = models.CharField(max_length=250, null=True, blank=True)
    '''quận huyện'''
    district = models.ForeignKey(districts, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''mã quận huyện'''
    district_code = models.CharField(max_length=250, null=True, blank=True)
    '''xã phường'''
    ward = models.ForeignKey(wards, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''mã xã phường'''
    ward_code = models.CharField(max_length=250, null=True, blank=True)
    '''fields: lĩnh vực công ty'''
    fields = models.CharField(max_length=250, blank=True, null=True)
    '''level của account'''
    level = models.ForeignKey(level_accounts, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''type: loại hình tổ chứa'''
    type = models.ForeignKey(type_company, on_delete=models.CASCADE, null=True)
    '''Email của account'''
    emails = models.CharField(max_length=150, blank=True, null=True)
    '''Số nhân viên [list string]'''
    employee = models.ForeignKey(employees, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''số điện thoại [list string]'''
    phones = models.CharField(max_length=150, blank=True, null=True)
    '''tiềm năng'''
    potential = models.ForeignKey(potentials, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''Vốn đầu từ'''
    investment = models.ForeignKey(capital_investments, on_delete=models.CASCADE, default=None, blank=True, null=True)
    '''is_del: check đã xóa hay chưa
    # 0: chưa
    # 1: đã xóa'''
    is_del = models.IntegerField(default=0)
    '''Ngày tạo'''
    created_date = models.IntegerField(default=Timer.get_timestamp_now())
    '''Ngày update'''
    update_date = models.IntegerField(default=Timer.get_timestamp_now())

    def __str__(self):
        return 'name: ' + self.name + ' - mst: ' + self.tax_code




