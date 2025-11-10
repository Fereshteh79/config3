from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from .models import Article
from .forms import ProfileForm, ArticleForm


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'account/article_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'account/article_create_update.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account:home')


class ArticleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'account/article_confirm_delete.html'
    success_url = reverse_lazy('account:home')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_superuser or obj.author == self.request.user


class Profile(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'account/profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account:profile')
