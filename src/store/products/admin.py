from django.contrib import admin

from .models import Product, Comment


admin.site.register(Product)
admin.site.register(Comment)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ["name", "price"]
#     list_editable = ["price"]

# python manage.py createsuperuser
