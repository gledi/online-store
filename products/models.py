from django.db import models

# create table products_product()
class Product(models.Model):
    # name varchar(255) not null
    name = models.CharField(max_length=255, null=False)
    # price decimal(6, 2) not null
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    description = models.TextField(null=True)
