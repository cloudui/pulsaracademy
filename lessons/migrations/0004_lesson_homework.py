# Generated by Django 2.2.7 on 2020-06-07 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20200603_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='homework',
            field=models.TextField(blank=True),
        ),
    ]
