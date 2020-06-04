
from django.urls import path, include

from .views import HomePageView, AboutPageView, InstructorPageView, RegistrationDetails

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('instructors/', InstructorPageView.as_view(), name='instructors'),
    path('registration/info/', RegistrationDetails.as_view(), name='registration_info'),
]