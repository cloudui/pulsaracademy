# Generated by Django 2.2.7 on 2021-01-17 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0019_class_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='completed',
            new_name='archived',
        ),
    ]
