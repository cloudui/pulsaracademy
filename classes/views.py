from django.shortcuts import render

from django.views.generic import ListView, DetailView, FormView

from .forms import ClassRegistrationForm, ClassUnregisterForm, ClassPaymentForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from random import randrange

from .models import Payment, Class

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
        # query class name from slug (can be changed)
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        
        # create the relationship
        payment = Payment(theclass=class_, user=self.request.user, cost=class_.cost)

        payment.save()

        # Class.register(self.request.user, class_)
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
        
        # delete the relationship
        m2 = Payment.objects.get(user=self.request.user, theclass=class_)
        # print("BEEGLEBEEGLE")
        # print(m2.id)
        # print(type(m2.id))
        # for payment in self.request.user.payment_set.all():
        #     print(payment.id) 
        m2.delete()
        
        return super(ClassUnregisterView, self).form_valid(form)


class ClassPaymentView(LoginRequiredMixin, ListView, FormView):
    model = Class
    form_class = ClassPaymentForm
    template_name = 'classes/payment.html'
    success_url = reverse_lazy('profile')
    login_url = 'account_login'


def class_checkout_view(request):
    invoice_id = ""
    separator = '|'

    for payment in request.user.payment_set.all():
        invoice_id = separator.join(str(payment.id))
    

    amount = str(request.user.payment_owed())

    # this is the payment information that paypal will use for redirect
    paypal_dict = {
        "business": "bigchungus123@gmail.com",
        "amount": amount,
        "item_name": "name of the item",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse_lazy('checkout')),
        "cancel_return": request.build_absolute_uri(reverse_lazy('checkout')),
   
    }


    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "classes/payment.html", context)

    

class CheckoutSummaryView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'classes/summary.html'
    login_url = 'account_login'

