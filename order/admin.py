from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['__str__','variant_name','variant_price','quantity','total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__','status','final_price','discount','created_at','updated_at']
    list_filter = ['created_at','updated_at','status','final_price']
    search_fields = ['__str__','status','discount']
