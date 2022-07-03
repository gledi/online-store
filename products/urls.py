from django.urls import path

from . import views


# app_name = "products"

urlpatterns = [
    # path("", views.get_products, name="product_list"),
    path("", views.ProductListView.as_view(), name="product_list"),
    path("add/", views.product_add, name="product_add"),
    path("<int:pk>/", views.get_product_details, name="product_details"),
]
