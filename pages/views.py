from django.shortcuts import render

from django.views.generic import TemplateView, FormView
from .forms import ContactPageForm

from django.urls import reverse_lazy

from .emails import contact_email

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'test.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'

class RegistrationDetails(TemplateView):
    template_name = 'registration_info.html'

class InstructorPageView(TemplateView):
    template_name = 'instructors.html'

class TermsPageView(TemplateView):
    template_name = 'terms_and_conditions.html'

def error404_view(request, exception):

    return render(request, 'error404.html')
    

def error403_view(request, exception):

    return render(request, 'error403.html')
    

class ContactPageView(FormView):

    template_name = 'contact.html'
    form_class = ContactPageForm
    success_url = reverse_lazy('success_contact')
    def form_valid(self, form):

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        contact_email(first_name, last_name, email, message)

        return super().form_valid(form)

    


class SuccessContactPageView(TemplateView):

    template_name = 'success_email.html'


class TemporaryNotificationView(TemplateView):
    template_name = 'notification.html'
