from django.urls import path
from . import views

urlpatterns = [

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Fake Payment Gateway
    path(
        "payment/",
        views.payment,
        name="payment"
    ),

    # Payment Success
    path(
        "payment-success/",
        views.payment_success,
        name="payment_success"
    ),

    # Create Order
    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),

    # My Orders
    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),

]