# Generated by Django 4.1.3 on 2023-07-15 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planet1032", "0002_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="type",
            field=models.CharField(
                choices=[
                    ("E", "educational article"),
                    ("F", "Fiction"),
                    ("G", "Graphics"),
                    ("O", "Other"),
                ],
                default="O",
                max_length=1,
            ),
        ),
    ]
