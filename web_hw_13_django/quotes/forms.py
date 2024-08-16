from django import forms
from django.forms import models

from .models import Tag, Author, Quote


class TagForm(models.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class AuthorForm(models.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        widgets = {
            "born_date": forms.DateInput()
        }


class QuoteForm(models.ModelForm):
    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]
        widgets = {
            "tag": forms.CheckboxSelectMultiple(),
        }
