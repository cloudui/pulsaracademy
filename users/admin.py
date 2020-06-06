from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


from .forms import CustomUserCreationForm, CustomUserChangeForm

from .signupform import CustomSignupForm


CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'school', 'parent_email', 'grade']
    


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(UserProfile)
