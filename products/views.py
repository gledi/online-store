from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import Product, Comment
from .forms import CommentForm, Comment2Form, ProductForm


def get_products(request: HttpRequest) -> HttpResponse:
    page_number = int(request.GET.get("page", "1"))
    page_size = int(request.GET.get("size", "10"))

    if page_size < 5 or page_size > 100:
        raise ValueError("Invalid page size")

    products = Product.objects.all()
    paginator = Paginator(products, page_size)
    page = paginator.page(page_number)
    return render(request, "products/product_list.html", context={
        "products": products,
        "paginator": paginator,
        "page": page
    })


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 10
    page_kwarg = "page"


def get_product_details(request: HttpRequest, pk: int) -> HttpResponse:
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = Comment2Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            # comment = Comment(
            #     author=form.cleaned_data["name"],
            #     comment=form.cleaned_data["comment"],
            #     rating=form.cleaned_data["rating"],
            #     product=product,
            # )
            # comment.save()
            # comment = Comment.objects.create(
            #     author=form.cleaned_data["name"],
            #     comment=form.cleaned_data["comment"],
            #     rating=form.cleaned_data["rating"],
            #     product=product,
            # )
            return redirect("product_details", pk=pk)
    else:
        form = Comment2Form()

    return render(request, "products/product_details.html", context={
        "product": product,
        "form": form
    })


@login_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("product_details", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "products/product_add.html", context={
        "form": form
    })
