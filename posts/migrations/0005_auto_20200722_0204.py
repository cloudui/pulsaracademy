# Generated by Django 2.2.7 on 2020-07-22 06:04

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200606_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]