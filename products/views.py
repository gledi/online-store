from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from .models import Product, Comment
from .forms import CommentForm, Comment2Form, ProductForm


def get_products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    return render(request, "products/product_list.html", context={
        "products": products
    })
    # select id, name, price, description from products_product


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
