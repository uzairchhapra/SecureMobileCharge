from django.contrib import admin
from .models import *

class ChargeStationAdmin(admin.ModelAdmin):
    list_display = ['id','latitude', 'longitude']
    search_fields=['name','description','latitude','longitude']
    
class UserAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','email']    
    search_fields=['id','first_name','last_name','email']

class BookAdmin(admin.ModelAdmin):
    list_display = ['id','uid', 'cid','book_start_time','book_end_time']
    list_filter = ['id','uid', 'cid','book_start_time','book_end_time']
    search_fields=['id','uid', 'cid','book_start_time','book_end_time']



admin.site.register(ChargeStation,ChargeStationAdmin)

admin.site.register(UserOfApp,UserAdmin)
admin.site.register(Book,BookAdmin)

admin.site.site_header = "ChargingBuddy Admin"
admin.site.site_title = "Admin Page"
admin.site.index_title = "ChargingBuddy Admin Page"

