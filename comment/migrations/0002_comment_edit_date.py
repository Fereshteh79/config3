# Generated by Django 2.0.2 on 2018-08-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="edit_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
