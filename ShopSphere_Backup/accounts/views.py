from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from products.models import Product
from cart.models import Cart
from favorites.models import Favorite
from orders.models import Order

from .models import Profile
from .forms import ProfileForm


# --------------------
# Home Page
# --------------------
def home(request):

    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category:
        products = products.filter(category=category)

    return render(request, "index.html", {
        "products": products,
    })


# --------------------
# Register
# --------------------
def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(request, "register.html", {
        "form": form
    })


# --------------------
# Login
# --------------------
def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(request, "login.html", {
        "form": form
    })


# --------------------
# Logout
# --------------------
def user_logout(request):

    logout(request)

    return redirect("home")


# --------------------
# Profile
# --------------------
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = ProfileForm(instance=profile)

    order_count = Order.objects.filter(
        user=request.user
    ).count()

    cart_count = Cart.objects.filter(
        user=request.user
    ).count()

    wishlist_count = Favorite.objects.filter(
        user=request.user
    ).count()

    context = {

        "profile": profile,

        "form": form,

        "order_count": order_count,

        "cart_count": cart_count,

        "wishlist_count": wishlist_count,

    }

    return render(
        request,
        "profile.html",
        context
    )