# Generated by Django 4.1.3 on 2023-07-18 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planet1032", "0019_alter_userprofile_gender_chapter"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="images",
            field=models.ManyToManyField(blank=True, to="planet1032.image"),
        ),
        migrations.AlterField(
            model_name="chapter",
            name="order",
            field=models.IntegerField(default=0),
        ),
    ]
