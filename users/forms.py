from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from allauth.account.forms import SignupForm
from .models import CustomUser, UserProfile





class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    
    parent_email = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Parent Email'}))

    school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'School'}))

    grade = forms.IntegerField(max_value=12, min_value=1)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'parent_email', 'school', 'grade',)

    
        
  


    
        


    
        


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

