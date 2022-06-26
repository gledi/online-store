import mistune
from django.db import models, transaction
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def html_content(self):
        md = mistune.Markdown(mistune.HTMLRenderer())
        return md.parse(self.content)