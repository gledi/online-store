from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Product


def get_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "product_list.html", context={
        "products": products
    })
    # select id, name, price, description from products_product
