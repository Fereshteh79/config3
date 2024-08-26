from django.contrib.auth import views
from django.urls import path
from .views import ArtileList, ArtileUpdate, ArticleDelete, Profile

app_name = "account"

urlpatterns = [
    path("", ArtileList.as_view(), name="home"),
    path("article/create", ArtileUpdate.as_view(), name="article_create"),
    path("article/update/<int:pk>", ArtileUpdate.as_view(), name="article_update"),
    path("article/delete/<int:pk>", ArticleDelete.as_view(), name="article_delete"),
    path("profile/", Profile.as_view(), name="profile"),
]
