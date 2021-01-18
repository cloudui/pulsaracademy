from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
import classes

from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    parent_email = models.EmailField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)

    grade = models.IntegerField(null=True)

    def payment_owed(self):
        payment = 0
        for course in self.classes_not_expired_registered_list():
            payment += course.cost
        
        return int(payment)

    
    def classes_paid_list(self):
        return self.class_set.all().filter(payment__paid=True).order_by('date')
    # def classes_paid_list(self):
    #     return self.class_set.all().filter(payment__paid=True)
    
    def classes_not_paid_list(self):
        return self.class_set.all().filter(payment__paid=False)

    def classes_confirmed_not_paid_list(self):
        
        courses = self.class_set.all().filter(payment__paid=False, confirmed=True)
        
        
        return courses
    
    def classes_expired_registered_list(self):

        return self.class_set.all().filter(payment__paid=False, confirmed=True, past_payment_deadline=True)
    
    def classes_not_expired_registered_list(self):
        return self.class_set.all().filter(payment__paid=False, confirmed=True, past_payment_deadline=False)
    
    def classes_registered_list(self):
        return self.class_set.all().filter(payment__paid=False, past_payment_deadline=False).order_by('date')

    # def classes_registered_list(self):
    #     return self.class_set.all().filter(payment__paid=False, past_payment_deadline=False)
    
        
    def payments_not_paid_list(self):
        return self.payment_set.all().filter(paid=False)
    
    def payments_pay_now(self):
        return self.payment_set.all().filter(paid=False, theclass__past_payment_deadline=False, theclass__confirmed=True)

    def num_payments_not_paid(self):
        num = len(self.classes_not_expired_registered_list())
        if num > 0:
            return f'({num})'
        return ''
    
    def num_users(self):
        return CustomUser.objects.all().count() - 2\
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

                       
    



class UserProfile(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    parent_email = models.CharField(max_length=100, null=True)

    school = models.CharField(max_length=200, null=True)
    grade = models.IntegerField(null=True)

    


    

