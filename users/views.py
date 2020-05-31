from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.

class ProfilePageView(TemplateView):
    template_name = 'profile.html'