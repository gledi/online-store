from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def contact_us(request):
    return render(request, "pages/contact_us.html")
