from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile

from classes.models import Payment

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .signupform import CustomSignupForm


CustomUser = get_user_model()


class PaymentInline(admin.TabularInline):
    model=Payment

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name','school', 'parent_email', 'grade']
    inlines = [  PaymentInline, ]


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(UserProfile)
