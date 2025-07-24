from django.views.generic import ListView, DetailView
from apps.cart.forms import AddToCartForm
from .models import Product, Category



class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(is_active=True)

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        self.search_term = self.request.GET.get("search", "").strip()
        self.category_slug = self.request.GET.get("category", "").strip()

        if self.search_term:
            qs = qs.filter(
                name__icontains=self.search_term
            )

        if self.category_slug:
            qs = qs.filter(category__slug=self.category_slug)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.search_term
        ctx["current_category"] = self.category_slug
        ctx["categories"] = Category.objects.all().order_by("name")
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = AddToCartForm()
        return ctx
