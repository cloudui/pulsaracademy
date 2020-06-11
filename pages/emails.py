


from django.core.mail import send_mail

from django.template import loader




def contact_email(first_name, last_name, email, message):
    subject = loader.get_template('email/contact_email_subject.txt').render({
        'first_name': first_name,
        'last_name': last_name,
    })
    message = loader.get_template('email/contact_email_message.txt').render({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'message': message,
    })

    send_mail(subject, message, 'inquiry@pulsaracademy.com', ['admin@pulsaracademy.com'])

