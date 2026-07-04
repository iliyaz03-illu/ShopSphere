from django.urls import path
from . import views

urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "payment/",
        views.payment,
        name="payment"
    ),

    path(
        "payment-success/",
        views.payment_success,
        name="payment_success"
    ),

    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "order/<int:order_id>/",
        views.order_details,
        name="order_details"
    ),

    path(
        "invoice/<int:order_id>/",
        views.invoice,
        name="invoice"
    ),

]