# src/main/tasks.py
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import  get_channel_layer
from django.core.mail import send_mail
from .models import MailTemplate
from src.user.models import BaseUser
from django.core.cache import cache



@shared_task
def send_mailing(mailing_id):
    cache.set("current_mailing", mailing_id)
    subject = "Тема"
    mailing_object = MailTemplate.objects.get(pk=mailing_id)
    recipients = BaseUser.objects.exclude(email='').values_list('email', flat=True)
    html_message = mailing_object.file.file.read().decode('utf-8')

    total = len(recipients)

    cache.set(f"mailing:{mailing_id}:progress", {
        "sent": 0,
        "total": total,
        "status": "running"
    })

    channel_layer = get_channel_layer()

    for i, email in enumerate(recipients, start=1):
        send_mail(
            subject="Тема",
            message='',
            from_email=None,
            recipient_list=[email],
            html_message=html_message
        )

        progress_data = {
            "sent": i,
            "total": total,
            "status": "running"
        }
        cache.set(f"mailing:{mailing_id}:progress", progress_data)

        async_to_sync(channel_layer.group_send)(
            f"mailing_{mailing_id}",
            {
                "type": "mailing.progress",
                "progress": int(i / total * 100),
                "sent": i,
                "total": total,
                "email": email
            }
        )

    cache.set(f"mailing:{mailing_id}:progress", {
        "sent": total,
        "total": total,
        "status": "finished"
    })
    cache.delete("current_mailing")



    async_to_sync(channel_layer.group_send)(
        f"mailing_{mailing_id}",
        {
            "type": "mailing.finished",
            "total": total
        }
    )


