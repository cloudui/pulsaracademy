
from django.urls import path, include

from .views import HomePageView, AboutPageView, InstructorPageView, RegistrationDetails, TermsPageView, ContactPageView, SuccessContactPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('instructors/', InstructorPageView.as_view(), name='instructors'),
    path('terms-and-conditions/', TermsPageView.as_view(), name='terms'),
    path('general/info/', RegistrationDetails.as_view(), name='registration_info'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('contact/success/', SuccessContactPageView.as_view(), name='success_contact'),
]