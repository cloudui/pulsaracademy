# Generated by Django 2.2.7 on 2021-01-17 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0018_auto_20200722_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
