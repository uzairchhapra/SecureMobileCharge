from django.contrib import admin
from .models import *

class ChargeStationAdmin(admin.ModelAdmin):
    list_display = ['id','latitude', 'longitude']
    search_fields=['name','description','latitude','longitude']

class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','email']



admin.site.register(ChargeStation,ChargeStationAdmin)


# Register your models here.
admin.site.register(UserOfApp,UserAdmin)
# admin.site.register(LogOfApp)

admin.site.site_header = "ChargingBuddy Admin"
admin.site.site_title = "Admin Page"
admin.site.index_title = "ChargingBuddy Admin Page"

