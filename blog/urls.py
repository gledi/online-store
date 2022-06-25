from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_post_list, name="post_list"),
]