from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from datetime import datetime, timedelta
from classes.models import Class

from django.utils import timezone

    
def x_ago_helper(diff):
    if diff.days // 365 >= 2:
        return f'{diff.days // 365} years ago'
    if diff.days // 365 == 1:
        return f'1 year ago'
    if diff.days // 30 >= 2:
        return f'{diff.days // 30} months ago'
    if diff.days // 30 == 1:
        return f'1 month ago'
    if diff.days > 1:
        return f'{diff.days} days ago'
    if diff.days == 1:
        return f'{diff.days} day ago'
    if diff.seconds < 60:
        return f'{diff.seconds} seconds ago'
    if diff.seconds // 60 == 1:
        return '1 minute ago'
    if diff.seconds < 3600:
        return f'{diff.seconds // 60} minutes ago'
    return f'{diff.seconds // 3600} hours ago'


class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=True)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    
    
    course = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
    )
        
    def x_ago(self):
        diff = timezone.now() - self.date
        return x_ago_helper(diff)
    def x_ago_updated(self):
        diff = timezone.now() - self.date_updated
        return x_ago_helper(diff)


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
    

class Comment(models.Model):
    body = models.TextField()

    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
    )
    valid = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def x_ago(self):
        diff = timezone.now() - self.date
        return x_ago_helper(diff)
    def x_ago_updated(self):
        diff = timezone.now() - self.date_updated
        return x_ago_helper(diff)

    def edited(self):
        time_difference = self.date_updated - self.date
        if abs(time_difference.total_seconds()) > 30:
            return True
        return False

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'Comment by { self.user.first_name } { self.user.last_name } on { self.post.title }'

