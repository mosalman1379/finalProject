import os

import weasyprint
from celery import shared_task
from django.conf import settings
from django.core.mail import  EmailMessage
from django.template.loader import render_to_string
from io import BytesIO


@shared_task
def send_mail_to(subject, Htmlpath, receivers,context):
    """
    celery task for sending email
    :param subject: subject of our email
    :param Htmlpath: the html path of whole email
    :param receivers: list of our receiver email
    :param context: context of own email
    :return: nothing
    """
    email=EmailMessage(subject=subject,body='Please, find attached the invoice for your recent',
                       from_email=settings.EMAIL_HOST_USER,to=[receivers])
    html_message=render_to_string(Htmlpath,{'context':context})
    out=BytesIO()
    stylesheets=[weasyprint.CSS(os.path.join(settings.STATIC_ROOT,'sale/static/css/pdf.css'))]
    weasyprint.HTML(string=html_message).write_pdf(out,stylesheets=stylesheets)
    email.attach(filename='Quote.pdf',content=out.getvalue(),mimetype='application/pdf')
    email.send()
