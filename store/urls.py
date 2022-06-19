from django.contrib import admin
from django.urls import path

from pages.views import home, about, privacy_policy, contact_us, details


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home),
    path("about", about),
    path("privacy-policy", privacy_policy),
    path("contact-us", contact_us),
    path("product", details)
]
