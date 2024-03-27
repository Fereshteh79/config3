from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .mixins import AuthorsAccessMixin
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperuserAccessMixin
from django.views.generic import ListView, UpdateView
from blog.models import Article
from .models import User
from .forms import ProfileForm


class ArtileList(AuthorsAccessMixin, ListView):
    template_name = "account/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArtileUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Article
    template_name = "account/article_create_update.html"


class ArticleDelete(SuperuserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("account:home")
    template_name = "account/article_confirm_delete.html"


class Profile(AuthorsAccessMixin, UpdateView):
    model = User
    success_url = reverse_lazy("account:Profile")
    template_name = "account/profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(ListView):
    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return  reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")
