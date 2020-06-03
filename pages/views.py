from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'

def error404_view(request, exception):

    return render(request, 'error404.html')

def error403_view(request, exception):

    return render(request, 'error403.html')
    