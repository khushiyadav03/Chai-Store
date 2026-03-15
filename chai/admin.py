from django.contrib import admin
from django.utils.html import format_html, format_html_join

from .models import (
    BulkOrderRequest,
    ChaiCertificate,
    ChaiReview,
    ChaiVariety,
    ContactMessage,
    MenuItem,
    SiteContent,
    Store,
    Testimonial,
)


class ChaiReviewInline(admin.TabularInline):
    model = ChaiReview
    extra = 1


@admin.register(ChaiVariety)
class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "date_added")
    list_filter = ("type", "date_added")
    search_fields = ("name", "description")
    inlines = [ChaiReviewInline]


@admin.register(ChaiReview)
class ChaiReviewAdmin(admin.ModelAdmin):
    list_display = ("chai", "user", "rating", "date_added")
    list_filter = ("rating", "date_added")
    search_fields = ("chai__name", "user__username", "comment")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "tag", "is_available")
    list_filter = ("category", "tag", "is_available")
    search_fields = ("name", "description")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "phone", "opening_hours")
    list_filter = ("city",)
    search_fields = ("name", "address", "city", "phone")
    exclude = ("location", "chai_varities")
    readonly_fields = ("available_menu_items",)
    fields = ("name", "address", "city", "phone", "opening_hours", "google_maps_url", "available_menu_items")

    def available_menu_items(self, obj):
        menu_items = MenuItem.objects.filter(is_available=True).values_list("name", "category")
        if not menu_items:
            return "No available menu items found."
        return format_html(
            "<div>{}</div>",
            format_html_join("", "<p>{} <span style='color:#5f6b7a;'>({})</span></p>", ((name, category) for name, category in menu_items)),
        )

    available_menu_items.short_description = "Menu items auto-fetched from MenuItem"


@admin.register(ChaiCertificate)
class ChaiCertificateAdmin(admin.ModelAdmin):
    list_display = ("chai", "certificate_num", "issued_date", "valid_till")
    list_filter = ("issued_date", "valid_till")
    search_fields = ("chai__name", "certificate_num")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating")
    list_filter = ("rating",)
    search_fields = ("customer_name", "quote")


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ("key", "value")
    search_fields = ("key", "value")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "submitted_at")
    list_filter = ("submitted_at",)
    search_fields = ("name", "email", "phone", "message")


@admin.register(BulkOrderRequest)
class BulkOrderRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "org", "quantity", "date", "submitted_at")
    list_filter = ("date", "submitted_at")
    search_fields = ("name", "org", "message")
