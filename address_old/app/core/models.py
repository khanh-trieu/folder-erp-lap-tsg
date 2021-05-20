from django.db import models

# Create your models here.
class currencies(models.Model):
    code = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    symbol = models.CharField(max_length=250, blank=True)

    def create_or_no_update(self):
        arr = []
        for i in self:
            item = currencies.objects.filter(code=i['code'])
            if not item:
                item_new = currencies.objects.create(code=i['code'], name=i['name'], symbol=i['symbol'] if i['symbol'] != None else '')
                arr.append(item_new.id)
            else:
                arr.append(item.first().id)
        # item = currencies.objects.filter(code=self['code'])
        # if item:
        #     item_new = currencies.objects.create(code=self['code'],name=self['name'],symbol=self['symbol'])
        #     return item_new
        return arr

    def __str__(self):
        return self.name + ' - ' + self.code


class languages(models.Model):
    iso639_1 = models.CharField(max_length=250, blank=True,null=True)
    iso639_2 = models.CharField(max_length=250, blank=True,null=True)
    name = models.CharField(max_length=250, blank=True,null=True)
    nativeName = models.CharField(max_length=250, blank=True,null=True)

    def create_or_no_update(self):
        arr = []
        for i in self:
            item = languages.objects.filter(name=i['name'])
            if not item:
                item_new = languages.objects.create(name=i['name'], iso639_1=i['iso639_1'], iso639_2=i['iso639_2'], nativeName=i['nativeName'])
                arr.append(item_new.id)
            else:
                arr.append(item.first().id)
        # item = currencies.objects.filter(code=self['code'])
        # if item:
        #     item_new = currencies.objects.create(code=self['code'],name=self['name'],symbol=self['symbol'])
        #     return item_new
        return arr

    def __str__(self):
        return self.name + ' - ' + self.nativeName


class countrys(models.Model):
    name = models.CharField(max_length=250, blank=True,null=True)
    code = models.CharField(max_length=250, blank=True,null=True)
    callingCodes = models.CharField(max_length=250, blank=True,null=True)
    capital = models.CharField(max_length=250, blank=True,null=True)
    region = models.CharField(max_length=250, blank=True,null=True)
    subregion = models.CharField(max_length=250, blank=True,null=True)
    demonym = models.CharField(max_length=250, blank=True,null=True)
    area = models.CharField(max_length=250, blank=True,null=True)
    timezones = models.CharField(max_length=250, blank=True,null=True)
    nativeName = models.CharField(max_length=250, blank=True,null=True)
    numericCode = models.CharField(max_length=250, blank=True,null=True)
    population = models.CharField(max_length=250, blank=True,null=True)
    flag = models.CharField(max_length=250, blank=True,null=True)
    currencies = models.ManyToManyField(currencies,  default=None, blank=True, null=True)
    languages = models.ManyToManyField(languages, default=None, blank=True, null=True)


class provinces(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    country = models.ForeignKey(countrys, on_delete=models.CASCADE, default=None, blank=True, null=True)


class districts(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    province = models.ForeignKey(provinces, on_delete=models.CASCADE, default=None, blank=True, null=True)


class wards(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    district = models.ForeignKey(districts, on_delete=models.CASCADE, default=None, blank=True, null=True)
