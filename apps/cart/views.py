from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddToCartForm, CheckoutForm
from .models import Cart, CartItem
from apps.product.models import Product
from apps.order.models import OrderItem, Order
from apps.payment.models import Payment


def _get_cart(request):
    """Helper: retorna (y crea) el carrito del usuario autenticado."""
    cart, _ = Cart.objects.get_or_create(user=request.user)  # One‑to‑One
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        cart = _get_cart(request)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += quantity
        item.save()
    return redirect("cart")


@login_required
def cart_view(request):
    cart = _get_cart(request)
    total = sum(item.get_total_price() for item in cart.items.all())
    return render(request, "cart.html", {"cart": cart, "total": total})


@login_required
def checkout_view(request):
    cart = _get_cart(request)
    if not cart.items.exists():
        return redirect("product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, status="PAID")
            order_items = [
                OrderItem(order=order,
                          product=item.product,
                          quantity=item.quantity,
                          unit_price=item.product.price)
                for item in cart.items.all()
            ]
            OrderItem.objects.bulk_create(order_items)

            total = sum(oi.get_total_price() for oi in order_items)
            Payment.objects.create(order=order, amount=total,
                                   payment_method=form.cleaned_data["payment_method"])

            cart.items.all().delete()  # Vaciar carrito
            return redirect("order_summary", order_id=order.id)
    else:
        form = CheckoutForm()

    total = sum(item.get_total_price() for item in cart.items.all())
    return render(request, "checkout.html", {"form": form, "total": total})

