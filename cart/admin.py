from django.contrib import admin
from .models import Cart, CartItem, Discount, DiscountUsage

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product','variant','quantity']

class DiscountUsageInline(admin.TabularInline):
    model = DiscountUsage
    extra = 0
    readonly_fields = ['user','used_at','order_id']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__','created_at','updated_at']
    search_fields = ['user']
    inlines = [CartItemInline]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['__str__','is_active','expires_at','max_uses']
    inlines = [DiscountUsageInline]
    list_filter = ['is_active','expires_at']
    search_fields = ['code']
