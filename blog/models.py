from django.db import models
from django.urls import reverse
from account.models import User
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")


class CategoryManager(models.Manager):
    def published(self):
        return self.filter(status=True)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')


class Category(models.Model):
    parents = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="زیر دست",
    )
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(default=0, verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["parents__id", "position"]

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ("d", "Draft"),
        ("p", "Published"),
        ("i", "درحال بررسی"),  # investigation
        ("b", "برگشت داده شده"),  # back
    )
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="articles",
        verbose_name="نویسنده",
    )
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس مقاله")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name="articles"
    )
    descriptions = models.TextField(blank=True, null=True, verbose_name="محتوا")
    thumbnail = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="تصویر مقاله"
    )
    published = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت"
    )
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through_fields="ArticleHit", blank=True, related_name='hits',
                                  verbose_name='بازدید ها')

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"
        ordering = ["-published"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:home")

    def jpublished(self):
        return jalali_converter(self.published)

    jpublished.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html(
            "<img width=100px; height=75px; style=border-radius: 5px; src='{}'>".format(
                self.thumbnail.url
            )
        )

    thumbnail_tag.short_description = "عکس"

    def category_to_str(self):
        return "،".join([category.title for category in self.category.active()])

    category_to_str.short_description = "دسته یندی"

    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
