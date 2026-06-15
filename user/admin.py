from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ['province', 'city', 'postal_code', 'is_default']

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['is_active', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional information', {
            'fields': ('phone_number', 'avatar', 'national_code', 'birth_date')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional information', {
            'fields': ('phone_number', 'avatar', 'national_code', 'birth_date')
        }),
    )

    inlines = [AddressInline] # this will show the addresses for one user in admin panel

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'province', 'city', 'postal_code', 'is_default']

    fieldsets = (
    ('user info', {
        'fields': ('user', 'is_default')
    }),
    ('اطلاعات آدرس', {
        'fields': ('province', 'city','building_number', 'unit', 'postal_code')
    }),
    )



