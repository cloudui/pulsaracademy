
from django.core.mail import EmailMessage

from django.core.mail import send_mail

from django.template import loader
from pythoncamp_project.settings import DEFAULT_FROM_EMAIL

def test_email_send():
    subject = loader.get_template('email/test_subject.txt').render({})
    message = loader.get_template('email/test_message.txt').render({
        'name': 'Eric',
        'like': 'pie'
    })

    send_mail(subject, message, DEFAULT_FROM_EMAIL, ['ericchen314@gmail.com'])



    

