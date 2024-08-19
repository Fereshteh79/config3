from django.contrib import admin
from .models import Article, Category


# admin.site.disable_action('delete_selected')


def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status="p")
    if rows_updated == 1:
        message_bit = "منتشر شد"
    else:
        message_bit = "منتشر شدند"
        modeladmin.massege_user(request, "{} مقاله {}".format())
    make_published.short_description = "انتشار مقالات انتخاب شده"


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status="d")
    if rows_updated == 1:
        message_bit = "پیش نویس شد"
    else:
        message_bit = "پیش نویس شدند"
        modeladmin.massege_user(request, "{} مقاله {}".format())


make_draft.short_description = "پیش نویس شدن مقالات انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "slug", "parents", "status")
    list_filter = ["status"]
    search_fields = ("title", "descriptions")
    prepopulated_fields = {"slug": ("title",)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "thumbnail",
        "slug",
        "author",
        "jpublished",
        "is_special",
        "status",
        "get_categories",
    )
    list_filter = ("published", "status", "author")
    search_fields = ("title", "descriptions")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["-status", "-published"]
    actions = [make_published, make_draft]

    @admin.display(description="دسته بندی ها")
    def get_categories(self, obj):
        return [category.title for category in obj.category.all()]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
