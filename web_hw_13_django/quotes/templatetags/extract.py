from ..models import Author
from bson import ObjectId
from django import template

register = template.Library()


def get_author(id_):
    author = Author.objects.get(id=id_)
    return author['fullname']


register.filter("author", get_author)
