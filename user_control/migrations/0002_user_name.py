# Generated by Django 5.0.4 on 2024-04-17 08:20

from django.db import migrations, models  # type: ignore


class Migration(migrations.Migration):

    dependencies = [
        ("user_control", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="None", max_length=500),
        ),
    ]
