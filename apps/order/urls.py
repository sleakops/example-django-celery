from django.urls import path

from . import views

urlpatterns = [
    path("pedido/<int:order_id>/", views.order_summary_view, name="order_summary"),
]