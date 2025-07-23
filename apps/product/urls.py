from django.urls import path

from . import views

urlpatterns = [
    path("productos/", views.ProductListView.as_view(), name="product_list"),
    path("producto/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
]