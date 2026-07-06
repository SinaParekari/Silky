from django.contrib import admin
from .models import (
    Weblog,
    WeblogCategory,
    WeblogText,
    WeblogReview,
    WeblogLike,
    WeblogTag,
    WeblogRelatedProduct
)
from django.forms.models import BaseInlineFormSet
from django.db.models import Max

# -----------------------------
# Inlines
# -----------------------------

class WeblogRelatedProductInline(admin.TabularInline):
    model = WeblogRelatedProduct
    extra = 1
    autocomplete_fields = ("product",)
    ordering = ("order",)

class WeblogTextInlineFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        obj = form.save(commit=False)

        max_order = (
            obj.weblog.texts.aggregate(Max("order"))["order__max"] or 0
        )
        obj.order = max_order + 1

        if commit:
            obj.save()
            form.save_m2m()

        return obj

class WeblogTextInline(admin.TabularInline):
    model = WeblogText
    formset = WeblogTextInlineFormSet
    extra = 1
    ordering = ("order",)
    fields = (
        "order",
        "template",
        "header",
        "text",
    )


class WeblogReviewInline(admin.TabularInline):
    model = WeblogReview
    extra = 0
    readonly_fields = ("created_at",)
    fields = (
        "user",
        "rating",
        "comment",
        "is_approved",
        "created_at",
    )


class WeblogLikeInline(admin.TabularInline):
    model = WeblogLike
    extra = 0
    readonly_fields = (
        "user",
        "created_at",
    )


# -----------------------------
# Category
# -----------------------------

@admin.register(WeblogCategory)
class WeblogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "title",
    )


# -----------------------------
# Tag
# -----------------------------

@admin.register(WeblogTag)
class WeblogTagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )

    search_fields = (
        "title",
    )

    filter_horizontal = (
        "weblog",
    )


# -----------------------------
# Weblog
# -----------------------------

@admin.register(Weblog)
class WeblogAdmin(admin.ModelAdmin):

    exclude = ("user",)

    inlines = [
        WeblogTextInline,
        WeblogRelatedProductInline,
        WeblogReviewInline,
        WeblogLikeInline,
        
    ]

    list_display = (
        "id",
        "title",
        "user",
        "category",
        "is_active",
        "views",
        "readTime",
        "likes_count",
        "reviews_count",
        "created_at",
    )

    list_filter = (
        "is_active",
        "category",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "summary",
        "excerpt",
        "slug",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "views",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    autocomplete_fields = (
        "category",
    )

    list_per_page = 20

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "category",
                    "is_active",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "excerpt",
                    "summary",
                    "image",
                )
            },
        ),
        (
            "Statistics",
            {
                "fields": (
                    "views",
                    "readTime",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Likes")
    def likes_count(self, obj):
        return obj.likes.count()

    @admin.display(description="Reviews")
    def reviews_count(self, obj):
        return obj.reviews.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "user",
            "category",
        ).prefetch_related(
            "likes",
            "reviews",
        )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user

        super().save_model(request, obj, form, change)


# -----------------------------
# Review
# -----------------------------

@admin.register(WeblogReview)
class WeblogReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "weblog",
        "user",
        "rating",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
        "created_at",
    )

    search_fields = (
        "weblog__title",
        "user__first_name",
        "user__last_name",
        "comment",
    )

    autocomplete_fields = (
        "weblog",
        "user",
    )

    readonly_fields = (
        "created_at",
    )

    actions = [
        "approve_reviews",
    ]

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)


# -----------------------------
# Like
# -----------------------------

@admin.register(WeblogLike)
class WeblogLikeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "weblog",
        "user",
        "created_at",
    )

    search_fields = (
        "weblog__title",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = (
        "weblog",
        "user",
    )

    readonly_fields = (
        "created_at",
    )


# -----------------------------
# Text
# -----------------------------

@admin.register(WeblogText)
class WeblogTextAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "weblog",
        "order",
        "template",
        "header",
    )

    list_filter = (
        "template",
    )

    search_fields = (
        "weblog__title",
        "header",
        "text",
    )

    autocomplete_fields = (
        "weblog",
    )

    ordering = (
        "weblog",
        "order",
    )