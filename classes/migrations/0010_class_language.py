# Generated by Django 2.2.7 on 2020-06-06 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0009_auto_20200605_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='language',
            field=models.CharField(choices=[('Django', 'Django'), ('Python', 'Python'), ('C++', 'C++'), ('Java', 'Java')], default='Python', max_length=50),
        ),
    ]
