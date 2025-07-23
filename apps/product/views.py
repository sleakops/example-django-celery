from django.views.generic import ListView, DetailView

from apps.cart.forms import AddToCartForm
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = AddToCartForm()
        return ctx
