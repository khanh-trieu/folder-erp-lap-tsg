from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(countrys)
admin.site.register(languages)
admin.site.register(currencies)