
from django import forms

# from crispy_forms.helper import FormHelper
class ContactPageForm(forms.Form):

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    message = forms.CharField(widget=forms.Textarea)

    # def __init__(self, *args, **kwargs):
    #     super(ContactPageForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_show_labels = False 
