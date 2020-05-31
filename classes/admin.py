from django.contrib import admin

# Register your models here.

from .models import Class

class ClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'show_users', )

    # def get_tournaments(self, obj):
    #     return "\n".join([p.users for p in obj.users.all()])


admin.site.register(Class, ClassAdmin)


