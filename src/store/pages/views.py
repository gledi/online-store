from django.shortcuts import render
from django.views.generic import TemplateView


# def page(request, name=None):
#     template_name = 'home' if name is None else name
#     return render(request, f"pages/{template_name.replace('-', '_')}.html")

class PageView(TemplateView):
    def get_template_names(self):
        name = self.kwargs.get("name", "home")
        template_name = f"pages/{name.replace('-', '_')}.html"
        return [template_name]
