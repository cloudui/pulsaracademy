from django.shortcuts import render

from django.views.generic import ListView, DetailView, FormView

from .forms import ClassRegistrationForm, ClassUnregisterForm, ClassPaymentForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from random import randrange


from .models import Class

from paypal.standard.forms import PayPalPaymentsForm

class ClassListView(ListView):
    template_name = 'classes/list.html'
    model = Class

class ClassDetailView(DetailView):
    template_name = 'classes/detail.html'
    model = Class


class ClassRegistrationView(LoginRequiredMixin, DetailView, FormView):
    model = Class
    form_class = ClassRegistrationForm
    template_name = 'classes/registration_detail.html'
    success_url = reverse_lazy('class_list')
    login_url = 'account_login'

    def form_valid(self, form):
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        Class.register(self.request.user, class_)
        return super(ClassRegistrationView, self).form_valid(form)

class ClassUnregisterView(LoginRequiredMixin, DetailView, FormView):
    model = Class
    form_class = ClassUnregisterForm
    template_name = 'classes/unregister_detail.html'
    success_url = reverse_lazy('class_list')
    login_url = 'account_login'

    def form_valid(self, form):
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        Class.unregister(self.request.user, class_)
        return super(ClassUnregisterView, self).form_valid(form)


class ClassPaymentView(LoginRequiredMixin, ListView, FormView):
    model = Class
    form_class = ClassPaymentForm
    template_name = 'classes/payment.html'
    success_url = reverse_lazy('profile')
    login_url = 'account_login'


def class_payment_view(request):
    user_name = request.user.first_name + request.user.last_name
    invoice_id = user_name + str(randrange(10000, 99999))

    paypal_dict = {
        "business": "bigchungus123@gmail.com",
        "amount": "10.00",
        "item_name": "name of the item",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment')),
        "cancel_return": request.build_absolute_uri(reverse('payment')),
   
    }


    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "classes/payment.html", context)

    