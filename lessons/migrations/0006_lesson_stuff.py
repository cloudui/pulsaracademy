# Generated by Django 2.2.7 on 2020-07-22 03:22

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_auto_20200721_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='stuff',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]
