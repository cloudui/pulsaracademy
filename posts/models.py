from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta
from classes.models import Class

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    
    
    course = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
    )
        


    # def save(self, *args, **kwargs):
        
    #     self.date_updated = datetime.now()

    #     super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    
    def edited(self):
        time_difference = self.date_updated - self.date
        if abs(time_difference.total_seconds()) > 30:
            return True
        return False

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.id)])
    