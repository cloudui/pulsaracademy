# Generated by Django 2.2.7 on 2020-06-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_class_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='instructor',
            field=models.CharField(choices=[('Eric Chen', 'Eric Chen'), ('Maxwell Zhang', 'Maxwell Zhang')], default='Eric Chen', max_length=50),
        ),
    ]
