from django.contrib import admin

from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'course', 'active',)


admin.site.register(Lesson, LessonAdmin)
