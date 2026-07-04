from django.urls import path
from .views import (
    add_to_cart,
    cart_view,
    remove_from_cart,
    increase_quantity,
    decrease_quantity,
)

urlpatterns = [
    path("", cart_view, name="cart"),

    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),

    path("remove/<int:cart_id>/", remove_from_cart, name="remove_from_cart"),

    path("increase/<int:cart_id>/", increase_quantity, name="increase_quantity"),

    path("decrease/<int:cart_id>/", decrease_quantity, name="decrease_quantity"),
]