from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView
from django.views.generic import DeleteView

from .forms import SignUpForm
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
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")


class Register(CreateView):
    form_class = SignUpForm
    template_name = "account/register.html"

    def form_valid(self, form, acccount_activation_token=None):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('account/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': acccount_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('<a href="/login">ورود</a>کد فعالسازی ایمیل شما ارسال شد.')
    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_encode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            if user not None and account_activation_token.check_token(user, token):
                user.is_active= True
                user.save()
                return HttpResponse('ایمیل شما با موفقیت فعال شد. برای ورود<a href="/login">کلیک</a>کنید')
            else:
                return HttpResponse('فعال سازی منقضی شده است.<a href="/account">دوباره امتحان کنید</a>')

