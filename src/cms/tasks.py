# src/main/tasks.py
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import  get_channel_layer
from django.core.mail import send_mail
from .models import MailTemplate
from src.user.models import BaseUser

@shared_task
def send_mailing(mailing_id):

    subject = "Тема"
    mailing_object = MailTemplate.objects.get(pk=mailing_id)
    recipients = BaseUser.objects.exclude(email='').values_list('email', flat=True)
    html_message = mailing_object.file.file.read().decode('utf-8')
    channel_layer = get_channel_layer()
    total = len(recipients)

    for i, email in enumerate(recipients, start=1):
        send_mail(
            subject="Тема",
            message='',
            from_email=None,
            recipient_list=[email],
            html_message=html_message
        )

        percent = int(i / total * 100)
        async_to_sync(channel_layer.group_send)(
            f"mailing_{mailing_id}",
            {
                "type": "mailing.progress",
                "email": email,
                "progress": percent
            }
        )


