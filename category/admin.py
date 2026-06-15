from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe
from .models import Category, CategoryAttribute


class CategoryAttbInline(admin.TabularInline):
    model = CategoryAttribute
    extra = 1
    fields = ['name', 'attribute_type', 'unit', 'is_filter', 'is_required']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CategoryAttbInline]

    readonly_fields = ['inherited_attributes']

    def inherited_attributes(self, obj):
        if not obj or not obj.parent:
            return "-"

        attrs = obj.parent.get_all_attributes()

        if not attrs:
            return "—"

        html = "".join(
            f"<div>{escape(attr.name)}</div>"
            for attr in attrs
        )

        return mark_safe(html)
    inherited_attributes.short_description = "Inherited Attributes"