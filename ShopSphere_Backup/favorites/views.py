from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Favorite
from products.models import Product


# ----------------------------
# Wishlist Page
# ----------------------------

@login_required
def favorite_list(request):

    favorites = Favorite.objects.filter(user=request.user)

    return render(request, "favorites.html", {
        "favorites": favorites
    })


# ----------------------------
# Add / Remove Favorite
# ----------------------------

@login_required
def toggle_favorite(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        favorite.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))