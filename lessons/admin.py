from django.contrib import admin

from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, LessonAdmin)
