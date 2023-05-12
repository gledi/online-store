from django.urls import path

from . import views


# app_name = "products"

urlpatterns = [
    # path("", views.get_products, name="product_list"),
    path("", views.ProductListView.as_view(), name="product_list"),
    path("add/", views.product_add, name="product_add"),
    path("<int:pk>/", views.get_product_details, name="product_details"),
    path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/publish/", views.approve_product, name="product_approve"),
    path("api/", views.ProductListAPIView.as_view(), name="api_product_list"),
]
