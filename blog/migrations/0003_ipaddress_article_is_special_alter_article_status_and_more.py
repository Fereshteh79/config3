# Generated by Django 4.1.7 on 2024-08-19 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_alter_article_options_article_author_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="IPAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField(verbose_name="آدرس آی پی")),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="is_special",
            field=models.BooleanField(default=False, verbose_name="مقاله ویژه"),
        ),
        migrations.AlterField(
            model_name="article",
            name="status",
            field=models.CharField(
                choices=[
                    ("d", "Draft"),
                    ("p", "Published"),
                    ("i", "درحال بررسی"),
                    ("b", "برگشت داده شده"),
                ],
                max_length=1,
                verbose_name="وضعیت",
            ),
        ),
        migrations.CreateModel(
            name="ArticleHit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.article"
                    ),
                ),
                (
                    "ip_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blog.ipaddress"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="article",
            name="hits",
            field=models.ManyToManyField(
                blank=True,
                related_name="hits",
                through="blog.ArticleHit",
                to="blog.ipaddress",
                verbose_name="بازدید ها",
            ),
        ),
    ]
