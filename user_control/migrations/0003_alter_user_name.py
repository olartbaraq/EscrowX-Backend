# Generated by Django 5.0.4 on 2024-04-18 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0002_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
