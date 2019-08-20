from django.contrib import admin
from .models import *
# Register your models here.

class ChargeStationAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude']


admin.site.register(ChargeStation,ChargeStationAdmin)
