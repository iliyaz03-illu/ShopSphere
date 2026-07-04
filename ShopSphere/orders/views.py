from decimal import Decimal
import random
import string

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order, Coupon, Payment
from .forms import ShippingForm


# =====================================================
# CHECKOUT
# =====================================================

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    total = Decimal("0.00")

    for item in cart_items:
        item.item_total = item.product.price * item.quantity
        total += item.item_total

    # Keep entered shipping data after POST
    if request.method == "POST":
        form = ShippingForm(request.POST)
    else:
        shipping_data = request.session.get("shipping")

        if shipping_data:
            form = ShippingForm(initial=shipping_data)
        else:
            form = ShippingForm()

    coupon_code = request.session.get("coupon", "")
    discount = Decimal("0.00")
    message = ""
    success = False

    # Restore saved coupon
    if coupon_code:

        try:

            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                active=True
            )

            discount = (
                total *
                Decimal(coupon.discount_percent)
            ) / Decimal("100")

        except Coupon.DoesNotExist:

            request.session.pop("coupon", None)

            coupon_code = ""

            discount = Decimal("0.00")

    # -----------------------------
    # Handle POST
    # -----------------------------
    if request.method == "POST":

        action = request.POST.get("action")

        coupon_code = request.POST.get(
            "coupon",
            ""
        ).strip()

        # ---------- APPLY COUPON ----------
        if action == "coupon":

            # Save shipping temporarily
            if form.is_valid():
                request.session["shipping"] = form.cleaned_data

            if coupon_code:

                try:

                    coupon = Coupon.objects.get(
                        code__iexact=coupon_code,
                        active=True
                    )

                    discount = (
                        total *
                        Decimal(coupon.discount_percent)
                    ) / Decimal("100")

                    request.session["coupon"] = coupon.code

                    message = "Coupon applied successfully."

                    success = True

                except Coupon.DoesNotExist:

                    request.session.pop("coupon", None)

                    coupon_code = ""

                    discount = Decimal("0.00")

                    message = "Invalid coupon."

            else:

                request.session.pop("coupon", None)

                message = "Please enter a coupon."

        # ---------- CONTINUE TO PAYMENT ----------
        elif action == "payment":

            if form.is_valid():

                request.session["shipping"] = form.cleaned_data

                if coupon_code:
                    request.session["coupon"] = coupon_code

                return redirect("payment")

            else:

                message = "Please fill all shipping details."

    grand_total = total - discount

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
            "discount": discount,
            "grand_total": grand_total,
            "coupon_code": coupon_code,
            "message": message,
            "success": success,
        }
    )

# =====================================================
# APPLY COUPON
# =====================================================




# =====================================================
# PAYMENT PAGE
# =====================================================

@login_required
def payment(request):

    # Shipping data must exist
    if "shipping" not in request.session:
        return redirect("checkout")

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    total = Decimal("0.00")

    for item in cart_items:
        total += item.product.price * item.quantity

    coupon_code = request.session.get("coupon", "")
    discount = Decimal("0.00")

    if coupon_code:

        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                active=True
            )

            discount = (
                total * Decimal(coupon.discount_percent)
            ) / Decimal("100")

        except Coupon.DoesNotExist:
            pass

    grand_total = total - discount

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        request.session["payment_method"] = payment_method

        return redirect("payment_success")

    return render(
        request,
        "payment.html",
        {
            "total": grand_total,
            "coupon_code": coupon_code,
            "discount": discount,
        }
    )


# =====================================================
# PAYMENT SUCCESS
# =====================================================

@login_required
def payment_success(request):

    transaction = "TXN" + "".join(

        random.choices(
            string.digits,
            k=10
        )

    )

    request.session["transaction"] = transaction

    return render(

        request,

        "payment_success.html",

        {

            "transaction": transaction

        }

    )


# =====================================================
# PLACE ORDER
# =====================================================

@login_required
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    shipping = request.session.get("shipping")

    if not shipping:
        return redirect("checkout")

    payment_method = request.session.get("payment_method", "UPI")

    coupon_code = request.session.get("coupon", "")

    total = Decimal("0.00")

    for item in cart_items:
        total += item.product.price * item.quantity

    discount = Decimal("0.00")

    # Apply coupon if available
    if coupon_code:
        try:
            coupon = Coupon.objects.get(
                code__iexact=coupon_code,
                active=True
            )

            discount = (
                total *
                Decimal(coupon.discount_percent)
            ) / Decimal("100")

        except Coupon.DoesNotExist:
            discount = Decimal("0.00")
            coupon_code = ""

    # CREATE ORDERS (Always)
    for item in cart_items:

        item_total = item.product.price * item.quantity

        item_discount = Decimal("0.00")

        if total > 0:
            item_discount = (
                item_total / total
            ) * discount

        final_price = item_total - item_discount

        order = Order.objects.create(

            user=request.user,

            product=item.product,

            quantity=item.quantity,

            total_price=final_price,

            full_name=shipping["full_name"],

            phone=shipping["phone"],

            address=shipping["address"],

            city=shipping["city"],

            state=shipping["state"],

            pincode=shipping["pincode"],

            coupon_code=coupon_code,

            discount=item_discount,

        )

        Payment.objects.create(

            order=order,

            payment_method=payment_method,

            transaction_id="TXN" + "".join(
                random.choices(
                    string.digits,
                    k=10
                )
            ),

            amount=final_price,

            payment_status="Paid",

        )

        # Reduce stock
        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()

    request.session.pop("shipping", None)
    request.session.pop("coupon", None)
    request.session.pop("payment_method", None)
    request.session.pop("transaction", None)

    return redirect("my_orders")

# =====================================================
# MY ORDERS
# =====================================================

@login_required
def my_orders(request):

    orders = Order.objects.filter(

        user=request.user

    ).order_by(

        "-ordered_at"

    )

    return render(

        request,

        "my_orders.html",

        {

            "orders": orders

        }

    )

# =====================================================
# ORDER DETAILS
# =====================================================

@login_required
def order_details(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    payment = Payment.objects.filter(
        order=order
    ).first()

    return render(

        request,

        "order_details.html",

        {

            "order": order,

            "payment": payment,

        }

    )

# =====================================================
# INVOICE
# =====================================================

@login_required
def invoice(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    payment = Payment.objects.filter(
        order=order
    ).first()

    return render(

        request,

        "invoice.html",

        {

            "order": order,

            "payment": payment,

        }

    )