from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    parent_email = models.CharField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)

    grade = models.IntegerField(null=True)

    def payment_owed(self):
        payment = 0
        for object in self.class_set.all():
            payment += object.cost
        
        return int(payment)
    



class UserProfile(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    parent_email = models.CharField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)
    grade = models.IntegerField(null=True)

    


    

