from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_post_list, name="post_list"),
    path("<slug>/", views.get_post_details, name="post_details"),
]