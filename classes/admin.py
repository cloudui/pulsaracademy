from django.contrib import admin

# Register your models here.

from .models import Class, Payment

class ClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', )

    # def get_tournaments(self, obj):
    #     return "\n".join([p.users for p in obj.users.all()])

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paid',)

admin.site.register(Class, ClassAdmin)


admin.site.register(Payment, PaymentAdmin)
