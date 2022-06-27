from flask_mail import Message
from flask import render_template
from . import mail

def mail_message(subject, template, to, **kwargs): #subject is subject, template is where we create the message body, to is the recipient, **kwargs are any keyword arguments
    sender_email = 'renderwes@gmail.com'

    email = Message(subject, sender=sender_email, recipients=[to]) 
    email.body = render_template(template + ".txt", **kwargs) #txt version
    email.html = render_template(template + ".html", **kwargs) #html version
    mail.send(email)