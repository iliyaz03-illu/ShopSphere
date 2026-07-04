from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product

from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.user = request.user

            review.product = product

            review.save()

    return redirect(
        "product_detail",
        pk=product.id
    )