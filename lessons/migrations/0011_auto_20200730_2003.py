# Generated by Django 2.2.7 on 2020-07-31 00:03

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_lesson_embedded_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='homework',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='summary',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
