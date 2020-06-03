from django.shortcuts import get_object_or_404
from .models import Payment
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
 
 
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        print("BEEGLEGEGELGELGLEGLELGE\nBEEGELGLEGLEGLEL")
        payments = []
        cost = 0
        # payment was successful

        print(ipn.invoice)
        for ids in ipn.invoice.split('|'):
            payment = get_object_or_404(Payment, id=int(ids))
            payments.append(payment)
            print(payment.cost)
            cost += payment.cost
        print(payments)
        
        
        if cost == int(ipn.mc_gross):
            print('entered')
            for payment in payments:
                print('happen')
                payment.paid = True
                payment.save()           