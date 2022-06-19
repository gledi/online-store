from django.urls import path

from . import views


urlpatterns = [
    path("", views.home),
    path("about", views.about),
    path("privacy-policy", views.privacy_policy),
    path("contact-us", views.contact_us),
]
