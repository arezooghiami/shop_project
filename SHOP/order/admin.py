from django.contrib import admin
from .models import *
# Register your models here.

class ItemInLines(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user','product','variant','quantity','price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','email','f_name','l_name','address','create','paid','get_price','code']
    list_filter = ['code']
    inlines = [ItemInLines]

class CopounAdmin(admin.ModelAdmin):
    list_display = ['code','start','end','discount','active']



admin.site.register(Order,OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon,CopounAdmin)