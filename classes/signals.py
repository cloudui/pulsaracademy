from django.shortcuts import get_object_or_404
from .models import Payment
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
 
# from paypal.standard.ipn.signals import payment_was_successful, payment_was_flagged

from .emails import send_payment_confirmation_email
 
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    print('Activate')
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
        
        course_names = []

        if cost == int(ipn.mc_gross):
            print('entered')
            for payment in payments:
                                  
                print('happen')
                payment.paid = True
                payment.save()    
                course_names.append(payment.theclass.name)

            user = payments[0].user

            emails = []
            user_email = user.email
            emails.append(user_email)
            if user.parent_email:
                user_parent_email = user.parent_email
                emails.append(user_parent_email)

            send_payment_confirmation_email(emails, course_names, cost, user)
        

valid_ipn_received.connect(payment_notification)

                



