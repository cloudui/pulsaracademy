
from django.core.mail import EmailMessage

from django.core.mail import send_mail

from django.template import loader
from pythoncamp_project.settings import DEFAULT_FROM_EMAIL

from django.core.mail import EmailMultiAlternatives

from django.utils.html import strip_tags

def test_email_send():
    subject = loader.get_template('email/test_subject.txt').render({})
    message = loader.get_template('email/test_message.txt').render({
        'name': 'Eric',
        'like': 'pie'
    })

    send_mail(subject, message, DEFAULT_FROM_EMAIL, ['ericchen314@gmail.com'])



def send_payment_confirmation_email(email_list, course_list, payment, user):
    subject = "Course Payment Receieved"
    message = loader.render_to_string('email/payment_confirmation_email_message.html', context={
        'user_name': user.first_name,
        'course_list': course_list,


    })
    message_plain = strip_tags(message)

    msg = EmailMultiAlternatives(subject, message_plain, DEFAULT_FROM_EMAIL, email_list)
    msg.attach_alternative(message, "text/html")
    msg.send()


