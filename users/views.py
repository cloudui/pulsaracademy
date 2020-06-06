from django.shortcuts import render

from django.views.generic import TemplateView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import PermissionDenied

from allauth.account.views import PasswordChangeView

from .models import CustomUser

from django.urls import reverse_lazy

class ProfilePageView(LoginRequiredMixin, TemplateView):
    login_url = 'account_login'
    template_name = 'profile.html'

class StaffListView(LoginRequiredMixin, ListView):
    model = CustomUser
    login_url = "account_login"
    template_name = "account/user_list.html"

    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)
    
class MyCustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    login_url = 'account_login'
    success_url = reverse_lazy('password_success')
    template_name = 'account/password_change.html'


class PasswordChangeSuccessfulView(TemplateView):

    template_name = 'account/password_success.html'

