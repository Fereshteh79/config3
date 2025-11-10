from datetime import datetime, timedelta

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.urls import reverse

from ..models import Article, Category

register = template.Library()


@register.simple_tag
def title():
    """عنوان سایت برای head"""
    return "وبلاگ جنگو"


@register.inclusion_tag("blog/partials/sidebar_categories.html")
def category_navbar():
    """دسته‌بندی‌ها برای navbar یا sidebar"""
    categories = Category.objects.filter(status=True).order_by("position")
    return {"categories": categories}


@register.inclusion_tag("blog/partials/sidebar_popular.html")
def popular_articles():
    """مقالات پر بازدید ماه اخیر"""
    last_month = datetime.today() - timedelta(days=30)
    articles = Article.objects.published().annotate(
        count=Count('hits', filter=Q(articlehit__created__gt=last_month))
    ).order_by('-count', '-published')[:5]
    return {"articles": articles, "title": "مقالات داغ ماه"}


@register.inclusion_tag("blog/partials/sidebar_hot.html")
def hot_articles():
    """مقالات با بیشترین کامنت ماه اخیر"""
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    articles = Article.objects.published().annotate(
        count=Count(
            'comments',
            filter=Q(comments__posted__gt=last_month, comments__content_type_id=content_type_id)
        )
    ).order_by('-count', '-published')[:5]
    return {"articles": articles, "title": "مقالات پر بازدید ماه"}


@register.inclusion_tag("account/partials/link.html")
def link(request, link_name, content, classes=""):
    """تگ لینک داینامیک برای account"""
    return {
        "request": request,
        "link_name": link_name,
        "link": reverse(f"account:{link_name}"), }
