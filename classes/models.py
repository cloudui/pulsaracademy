from django.db import models

from users.models import CustomUser
from datetime import datetime
from datetime import time
import lessons
from django.urls import reverse_lazy
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

day_of_week = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
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

    first_day = models.CharField(max_length=50, choices=day_of_week, default='Monday')
    

    second_day = models.CharField(max_length=50, choices=day_of_week, default='Monday')


    third_day_optional = models.CharField(max_length=50, choices=day_of_week, null=True)

    def get_days_week(self):
        return [self.first_day, self.second_day]

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
    
    
    def start_date_format(self):
        the_date = self.date - timezone.timedelta(seconds=1)

        return the_date.strftime('%-m/%d/%Y at %-I:%M %p')
    

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

    def registration_deadline(self):
        two_days = timezone.timedelta(days=2, seconds=1)
        deadline = self.date - two_days

        return deadline.strftime('%-m/%d/%Y at %-I:%M %p')
    def past_registration_deadline(self):
        two_days = timezone.timedelta(days=2)
        deadline = self.date - two_days

        if timezone.now() > deadline:
            return True
        return False


    
    def paid_users_list(self):
        
        students = self.users.filter(payment__paid=True)
        return students
    
    def registered_users_list(self):

        students = self.users.filter(payment__paid=False)

        return students

    
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

    def get_absolute_url(self):
        return reverse_lazy('class_detail', kwargs={'slug': self.slug})


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    theclass = models.ForeignKey(Class, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

    cost = models.FloatField(default=0)
    
    

    # apply_late_fee = models.BooleanField(default=False)

