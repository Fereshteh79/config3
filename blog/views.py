from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from blog.models import Article, Category
from account.mixins import AuthorAccessMixin
from account.models import User

class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 3
    template_name = "blog/list.html"

class ArticleDetail(DetailView):
    model = Article
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = getattr(self.request, 'ip_address', None)
        if ip_address and ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

class ArticlePreview(AuthorAccessMixin, DetailView):
    model = Article
    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Article, pk=pk)

class CategoryList(ListView):
    template_name = "blog/list.html"
    paginate_by = 3

    def get_queryset(self):
        self.category = get_object_or_404(Category.objects.active(), slug=self.kwargs.get("slug"))
        return self.category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

class AuthorList(ListView):
    template_name = "blog/author_list.html"
    paginate_by = 3

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs.get("username"))
        return self.author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context

class SearchList(ListView):
    template_name = "blog/search_list.html"
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        return Article.objects.filter(Q(descriptions__icontains=query) | Q(title__icontains=query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        return context
