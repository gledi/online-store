from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")

def contact_us(request):
    return render(request, "contact_us.html")


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


def details(request):
    product = Product("PS5", "750 EUR")
    return render(request, "details.html", context={
        "product": product
    })
