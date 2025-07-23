from celery import shared_task

from .models import Order


@shared_task
def order_process(order_id):
    order = Order.objects.get(id=order)
    print(f'Process order number # {order.id}')
    print(f"User {order.user.username} has placed an order with status {order.status}")
