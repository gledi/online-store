from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Product, Comment
from .forms import CommentForm, Comment2Form, ProductForm
from .serializers import ProductSerializer


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
    context_object_name = "products"
    paginate_by = 10
    page_kwarg = "page"
    queryset = Product.objects.order_by("-id").all()


def get_product_details(request: HttpRequest, pk: int) -> HttpResponse:
    product = Product.objects.select_related("user").get(pk=pk)

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
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("product_details", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "products/product_add.html", context={
        "form": form
    })


class ProductUpdateView(UpdateView):
    model = Product
    fields = [
        "name",
        "price",
        "description",
        "photo",
    ]

    def get_success_url(self):
        return reverse("product_details", kwargs=self.kwargs)


@permission_required("products.publish_product")
def approve_product(request, pk):
    # try:
    #     product = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     raise Http404("Not found")
    product = get_object_or_404(Product, pk=pk)
    product.is_published = True
    product.save()
    return redirect("product_details", pk=pk)


def get_product_list(request: HttpRequest) -> HttpResponse:
    products = Product.objects.filter(is_published=True).all()
    paginator = Paginator(products, per_page=10)
    page = paginator.page(1)
    serializer = ProductSerializer(page.object_list, many=True)
    return JsonResponse({"products": serializer.data})


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_published=True).all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
