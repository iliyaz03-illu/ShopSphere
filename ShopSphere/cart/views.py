from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Product


# =====================================
# Add to Cart
# =====================================
@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Stay on the page where the user clicked "Add to Cart"
    return redirect(request.META.get("HTTP_REFERER", "home"))


# =====================================
# Cart Page
# =====================================
@login_required
def cart_view(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        total += item.item_total

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "cart.html", context)


# =====================================
# Remove Item
# =====================================
@login_required
def remove_from_cart(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.delete()

    return redirect("cart")


# =====================================
# Increase Quantity
# =====================================
@login_required
def increase_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect("cart")


# =====================================
# Decrease Quantity
# =====================================
@login_required
def decrease_quantity(request, cart_id):

    cart_item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")