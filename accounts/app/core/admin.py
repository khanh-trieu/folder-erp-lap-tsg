from django.contrib import admin

# Register your models here.


from core.models import *

admin.site.register(accounts)
admin.site.register(employees)
admin.site.register(fields)
# admin.site.register(phone_type)
# admin.site.register(account_channel_phones)
# admin.site.register(account_channel_emails)
admin.site.register(provinces)
admin.site.register(districts)
admin.site.register(wards)
admin.site.register(countrys)
admin.site.register(type_company)
admin.site.register(level_accounts)
admin.site.register(capital_investments)
admin.site.register(potentials)
# admin.site.register(type_accounts)