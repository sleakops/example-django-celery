from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Order


@login_required
def order_summary_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_total = sum(item.get_total_price() for item in order.items.all())
    return render(request, "order_summary.html", {"order": order, "order_total": order_total})
