from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldsMixin:
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "title",
            "slug",
            "category",
            "description",
            "thumbnail",
            "published",
            "is_special",
            "status",
        ]
        if request.user.is_superuser:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        if self.request.user.is_superuser:
            self.obj = form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if self.obj.status != "i":
                self.obj.status = "d"
            self.obj.save()
        return super().form_valid(form)


class AuthorAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if (article.author == request.user and article.status in ["b", "d"]) \
                or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404("You don't have permission to access this page.")


class AuthorsAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_author:
                return super().dispatch(request, *args, **kwargs)
            return redirect("account:profile")
        return redirect("account:login")


class SuperuserAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404("You don't have permission to access this page.")
