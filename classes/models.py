from django.db import models

from users.models import CustomUser
from datetime import datetime
from datetime import time
import lessons
from django.utils import timezone

diff = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced')
)

instr = (
    ('Eric Chen', 'Eric Chen'),
    ('Maxwell Zhang', 'Maxwell Zhang')
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

    syllabus = models.TextField(null=True)

    confirmed = models.BooleanField(default=False)
    instructor = models.CharField(max_length=50, choices=instr, default="Eric Chen")
    
    slug = models.SlugField(null=False, unique=True, default=None)

    users = models.ManyToManyField(CustomUser, blank=True, through='Payment', through_fields=('theclass', 'user')) 

    past_payment_deadline = models.BooleanField(default=False)

    def is_ongoing(self):
        if timezone.now() > self.date and timezone.now() < self.end_date:
            return True
        return False
    def past(self):
        if timezone.now() > self.end_date:
            return True
        return False

    
    def later(self):
        if timezone.now() < self.date:
            return True
        return False
    
    def update_past_payment_deadline(self):
        now = timezone.now()
        if now > self.date:
            self.past_payment_deadline = True

            
        
        return self.past_payment_deadline
        
    

    def show_users(self):
        return ', '.join([a.email for a in self.users.all()])

    def start_date_string(self):
        return self.date.strftime("%m/%d/%Y")

    def end_date_string(self):
        return self.end_date.strftime("%m/%d/%Y")

    def cost_decimal(self):
        return round(self.cost)

    def start_time_convert(self):
        return self.start_time.strftime("%-I:%M %p")
    def end_time_convert(self):
        return self.end_time.strftime("%-I:%M %p")

    def past_registration_deadline(self):
        two_days = timezone.timedelta(days=2)
        deadline = self.date - two_days

        if timezone.now() > deadline:
            return True
        return False
    
    

    
    @classmethod
    def auto_populate_courses(cls, class_, num):
        for count in range(1, num+1):
            name = f'Class {count}'
            lesson = lessons.models.Lesson(course=class_, name=name, number=count)
            lesson.save()
    

    class Meta:
        ordering = ('date', )
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    theclass = models.ForeignKey(Class, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    cost = models.FloatField(default=0)
    
    

    # apply_late_fee = models.BooleanField(default=False)

