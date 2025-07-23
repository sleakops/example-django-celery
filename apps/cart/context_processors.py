# context_processors.py
def cart_count(request):
    if request.user.is_authenticated:
        from .models import CartItem
        return {"cart_count": CartItem.objects.filter(cart__user=request.user).count()}
    return {}
