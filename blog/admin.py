from django.contrib import admin

from .models import Post, Comment, Picture

admin.site.register(Comment)


# class PictureInline(admin.StackedInline):
class PictureInline(admin.TabularInline)
    model = Picture


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published"]
    list_editable = ["is_published"]
    inlines = [
        PictureInline
    ]
