from django.db import models

from users.models import CustomUser
from datetime import datetime

diff = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced')
)

class Class(models.Model):

    name = models.CharField(max_length=255)

    date = models.DateTimeField()
    end_date = models.DateTimeField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    difficulty = models.CharField(max_length=40, choices=diff, default='beginner') 

    cost = models.FloatField(null=True)
        
    description = models.TextField(null=True)
    
    slug = models.SlugField(null=False, unique=True, default=None)

    users = models.ManyToManyField(CustomUser, blank=True, through='Payment', through_fields=('theclass', 'user')) 


    # def show_users(self):
    #     return ', '.join([a.email for a in self.users.all()])

    def start_date_string(self):
        return self.date.strftime("%m/%d/%Y")

    def end_date_string(self):
        return self.end_date.strftime("%m/%d/%Y")

    def cost_decimal(self):
        return round(self.cost)

    @classmethod
    def register(cls, user, class_):
        print(class_.order_set, "BEEGLE")
        # class_.order_set.user_set.add(user)

    @classmethod
    def unregister(cls, user, class_):
        # class_.users.remove(user)
        pass

    class Meta:
        ordering = ('date', )


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    theclass = models.ForeignKey(Class, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    cost = models.FloatField(default=0)
    
    

    # apply_late_fee = models.BooleanField(default=False)

