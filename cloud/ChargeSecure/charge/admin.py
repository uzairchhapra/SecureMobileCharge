from django.contrib import admin
from .models import *

class ChargeStationAdmin(admin.ModelAdmin):
    list_display = ['id','latitude', 'longitude','name']
    search_fields=['name','description','latitude','longitude','name']

class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','email']
    search_fields=['id','first_name','last_name','email']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','uid', 'sid', 'phone_status', 'action', 'action_time']
    list_filter = ['id','uid', 'sid', 'phone_status', 'action', 'action_time']
    search_fields=['id','uid', 'sid', 'phone_status', 'action', 'action_time']

class SlotAdmin(admin.ModelAdmin):
    list_display = ['id','slot_number','cid','status']
    list_filter = ['id','slot_number','cid','status']
    search_fields=['id','slot_number','cid','status']



admin.site.register(ChargeStation,ChargeStationAdmin)

admin.site.register(UserOfApp,UserAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Slot,SlotAdmin)

admin.site.site_header = "ChargingBuddy Admin"
admin.site.site_title = "Admin Page"
admin.site.index_title = "ChargingBuddy Admin Page"
