from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from .models import Product

from reviews.models import Review
from reviews.forms import ReviewForm


def product_detail(request, pk):

    product = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.exclude(
        id=product.id
    )[:4]

    reviews = Review.objects.filter(
        product=product
    )

    average_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    form = ReviewForm()

    context = {

        "product": product,

        "related_products": related_products,

        "reviews": reviews,

        "average_rating": average_rating,

        "review_form": form,

    }

    return render(
        request,
        "product_detail.html",
        context
    )