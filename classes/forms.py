from django import forms
from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html
from posts.models import Post

from django.forms import ModelForm

class ClassRegistrationForm(forms.Form):
    pass

class ClassUnregisterForm(forms.Form):
    pass


class ClassPaymentForm(forms.Form):
    pass


class AutoPopulateLessonsForm(forms.Form):
    num = forms.IntegerField(max_value=50, min_value=1)

class ExtPayPalPaymentsForm(PayPalPaymentsForm):
    def render(self):
        form_open  = u'''<form action="%s" id="PayPalForm" method="post">''' % (self.get_endpoint())
        form_close = u'</form>'
        # format html as you need
        submit_elm = u'''<input type="image" name="submit" src="https://lh3.googleusercontent.com/-VXNFtwEk0AA/XtkdlvKTB5I/AAAAAAAAPFs/R4yJTsD_AbckvqYB-_LYfyoYL-EgsXvzQCK8BGAsYHg/s0/2020-06-04.png" alt="Submit" style="width: 200px;float:right" />'''
        return format_html(form_open+self.as_p()+submit_elm+form_close)
        
class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)