from django.contrib import admin
from .models import Order, Payment, Coupon


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
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-ordered_at",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_id",
        "order",
        "payment_method",
        "amount",
        "payment_status",
        "paid_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
    )

    search_fields = (
        "transaction_id",
        "order__user__username",
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

    search_fields = (
        "code",
    )