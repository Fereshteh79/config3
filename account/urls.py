from django.urls import path
from .views import ArticleList, ArticleUpdate, ArticleDelete, Profile
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path("", ArticleList.as_view(), name="home"),
    path("article/create/", ArticleUpdate.as_view(), name="article_create"),
    path("article/update/<int:pk>/", ArticleUpdate.as_view(), name="article_update"),
    path("article/delete/<int:pk>/", ArticleDelete.as_view(), name="article_delete"),
    path("profile/", Profile.as_view(), name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='account:login'), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password_reset_complete"),
]
