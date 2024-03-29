# Generated by Django 4.1.3 on 2023-07-17 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planet1032", "0013_article_summary"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="articles/images/"
            ),
        ),
        migrations.AlterField(
            model_name="article",
            name="body",
            field=models.TextField(blank=True, null=True),
        ),
    ]
