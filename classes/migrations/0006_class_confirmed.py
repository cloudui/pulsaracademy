# Generated by Django 2.2.7 on 2020-06-04 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0005_class_syllabus'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
