from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_mail_to(subject, Htmlpath, receivers,context):
    html_message=render_to_string(Htmlpath,{'context':context})
    plain_message=strip_tags(html_message)
    send_mail(subject, plain_message, EMAIL_HOST_USER, [receivers],
              fail_silently=False)

