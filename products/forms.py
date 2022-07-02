import re
from django import forms

from .models import Comment


re_personal_no = re.compile(r'^[A-Z]\d{8}[A-Z]$')


class CommentForm(forms.Form):
    name = forms.CharField(required=True, max_length=64, strip=True)
    rating = forms.IntegerField(required=True, min_value=1, max_value=5)
    comment = forms.CharField(widget=forms.Textarea)
    # personal_no = forms.CharField(min_length=10, max_length=10)
    #
    # def clean_personal_no(self):
    #     if not re_personal_no.match(self.cleaned_data["personal_no"]):
    #         raise forms.ValidationError("Invalid personal number")

class Comment2Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "author",
            "rating",
            "comment",
            # "product",
        ]