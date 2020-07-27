from django.db import models

from django.urls import reverse
from tinymce.models import HTMLField

from classes.models import Class

class Lesson(models.Model):
    name = models.CharField(max_length=255, null=True)
    number = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=False)
    summary = HTMLField(default='')

    
    date = models.DateTimeField()

    course = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, default='')
    
    homework = HTMLField(default='')

    
    
    def __str__(self):
        if self.name:
            return self.name
        return "potato"



 
