from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title
