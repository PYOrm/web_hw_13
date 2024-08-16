from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Author, Tag, Quote
from django.core.paginator import Paginator


# Create your views here.

def index(request, page=1):
    quotes = Quote.objects.all()
    item_per_page = 10
    paginator = Paginator(list(quotes), item_per_page)
    quote_on_page = paginator.page(page)
    return render(request, template_name="quotes/index.html", context={"quotes": quote_on_page})


class CreateTagView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Tag
    template_name = "quotes/createTag.html"
    form_class = TagForm
    success_url = "createTag"


class CreateAuthorView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Author
    template_name = "quotes/createAuthor.html"
    form_class = AuthorForm
    success_url = "createAuthor"


class CreateQuoteView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = Quote
    template_name = "quotes/createQuote.html"
    form_class = QuoteForm
    success_url = "createQuote"


# def author_view(request, fullname):
#     author = Author.objects.get(fullname=fullname)
#     return render(request, template_name="quotes/authorInfo.html", context={"author": author})

class AuthorView(DetailView):
    model = Author
    template_name = "quotes/authorInfo.html"
    context_object_name = "author"

    def get_object(self):
        return Author.objects.get(fullname=self.kwargs['fullname'])
