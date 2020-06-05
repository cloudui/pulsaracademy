#!/usr/bin/env python

from classes.models import Class

from django.utils import timezone

def update_day_status():
    objs = Class.objects.all()

    time = timezone.now()
    print('hello')

    for obj in objs:
        if time > obj.date:
            obj.past_payment_deadline = True
            obj.save()




