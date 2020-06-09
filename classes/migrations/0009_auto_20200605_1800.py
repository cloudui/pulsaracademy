# Generated by Django 2.2.7 on 2020-06-05 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0008_class_past_payment_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='first_day',
            field=models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Monday', max_length=50),
        ),
        migrations.AddField(
            model_name='class',
            name='second_day',
            field=models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], default='Monday', max_length=50),
        ),
        migrations.AddField(
            model_name='class',
            name='third_day_optional',
            field=models.CharField(choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=50, null=True),
        ),
    ]