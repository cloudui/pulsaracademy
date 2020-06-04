from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
import classes



# Create your models here.
class CustomUser(AbstractUser):
    parent_email = models.CharField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)

    grade = models.IntegerField(null=True)

    def payment_owed(self):
        payment = 0
        for course in self.classes_confirmed_not_paid_list():
            payment += course.cost
        
        return int(payment)

    
    def classes_paid_list(self):
        return self.class_set.all().filter(payment__paid=True)
    
    def classes_not_paid_list(self):
        return self.class_set.all().filter(payment__paid=False)

    def classes_confirmed_not_paid_list(self):
        return self.class_set.all().filter(payment__paid=False, confirmed=True)


    def payments_paid_list(self):
        return self.payment_set.all().filter(paid=True)
    def payments_not_paid_list(self):
        return self.payment_set.all().filter(paid=False)

    def num_payments_not_paid(self):
        num = self.payment_set.all().filter(paid=False, theclass__confirmed=True).count()
        if num > 0:
            return f'({num})'
        return ''
    
    

                       
    



class UserProfile(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    parent_email = models.CharField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)
    grade = models.IntegerField(null=True)

    


    

