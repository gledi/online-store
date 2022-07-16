from django.db import models, transaction
from django.db.models import Q
from django.conf import settings

# create table products_product()
class Product(models.Model):
    # name varchar(255) not null
    name = models.CharField(max_length=255, null=False)
    # price decimal(6, 2) not null
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    description = models.TextField(null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="products")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="products",
                             null=True, blank=True, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("publish_product", "Can publish product"),
        ]

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "price": str(self.price),
            "description": self.description,
            "photo": None if self.photo is None else self.photo.url,
            "user": None if self.user is None else {
                "id": self.user.pk,
                "username": self.user.username,
            }
        }


class Comment(models.Model):
    author = models.CharField(max_length=64)
    comment = models.TextField()
    email = models.EmailField(null=True, blank=True)
    rating = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        # db_table = "comments"
        constraints = [
            models.CheckConstraint(check=Q(rating__gte=1) & Q(rating__lte=5),
                                   name="chk_comments_rating")
        ]
