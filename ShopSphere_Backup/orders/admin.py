print("Orders admin loaded")

from django.contrib import admin
from .models import Order, Coupon


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "quantity",
        "total_price",
        "status",
        "ordered_at",
    )

    list_filter = (
        "status",
        "ordered_at",
    )

    search_fields = (
        "user__username",
        "product__name",
        "full_name",
        "phone",
        "city",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-ordered_at",
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "discount_percent",
        "active",
    )

    list_editable = (
        "discount_percent",
        "active",
    )