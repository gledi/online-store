from django.shortcuts import render

from .models import Post

def get_post_list(request):
    status = request.GET.get("status", "all")

    qs = Post.objects.all()
    if status == "published":
        qs = qs.filter(is_published=True)
    elif status == "unpublished":
        qs = qs.filter(is_published=False)

    posts = qs.all()
    return render(request, "blog/post_list.html", context={
        "posts": posts
    })


def get_post_details(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "blog/post_details.html", context={
        "post": post
    })
