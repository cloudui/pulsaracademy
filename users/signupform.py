
from allauth.account.forms import SignupForm, LoginForm
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Submit

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        self.helper.add_input(Submit('submit', 'Log In', css_class='btn btn-success'))
        
        
    
    class Meta:
        model = get_user_model()
        fields = ('email',)

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    
    parent_email = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Parent Email'}))

    school = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'School'}))

    grade = forms.IntegerField(max_value=12, min_value=1)
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
    
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'parent_email', 'school', 'grade',)