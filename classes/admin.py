from django.contrib import admin

# Register your models here.

from .models import Class, Payment, Introduction



class ClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'show_users')

    # def get_tournaments(self, obj):
    #     return "\n".join([p.users for p in obj.users.all()])

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'theclass', 'id', 'paid',)

class IntroductionAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'course',
    )

admin.site.register(Class, ClassAdmin)


admin.site.register(Payment, PaymentAdmin)

admin.site.register(Introduction, IntroductionAdmin)
