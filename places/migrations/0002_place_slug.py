# Generated by Django 4.2.3 on 2023-07-27 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="place",
            name="slug",
            field=models.SlugField(blank=True, unique=True, verbose_name="slug"),
        ),
    ]