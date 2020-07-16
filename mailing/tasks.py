from __future__ import absolute_import, unicode_literals
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject, html_message, to_email, from_email=None):
    plain_message = strip_tags(html_message)
    # msg = EmailMultiAlternatives(subject, plain_message, to=[to_email])
    # # msg.attach_alternative(html_message, "text/html")
    # msg.send()
    if not from_email:
        from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)