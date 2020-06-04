from django.db import models

from django.urls import reverse

from classes.models import Class

class Lesson(models.Model):
    name = models.CharField(max_length=255, null=True)
    number = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=False)
    summary = models.TextField(null=True)

    
    date = models.DateTimeField(auto_now_add=True)

    course = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        if self.name:
            return self.name
        return "potato"



 
