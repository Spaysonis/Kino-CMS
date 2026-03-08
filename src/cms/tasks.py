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
    cache.set("current_mailing", mailing_id) # state now

    subject = "Тема"
    template = MailTemplate.objects.get(pk=mailing_id) # Take template with db
    recipients = BaseUser.objects.exclude(email='').values_list('email', flat=True) # Take user(email) with db
    html_message = template.file.file.read().decode('utf-8')
    template_name = template.file.name
    total = len(recipients)

    progress_key = f"mailing:{mailing_id}:progress"
    meta_key = f"mailing:{mailing_id}:meta"

    # meta data
    cache.set(meta_key, {
        "template_name": template_name,

    })

    # start state
    cache.set(progress_key, {
        "sent": 0,
        "total": total,
        "status": "running"
    })



    channel_layer = get_channel_layer()

    for i, email in enumerate(recipients, start=1):
        send_mail(
            subject=subject,
            message='',
            from_email=None,
            recipient_list=[email],
            html_message=html_message
        )

        cache.set(progress_key, {
            "sent": i,
            "total": total,
            "status": "running",
        })

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
    #cache.delete("current_mailing")



    async_to_sync(channel_layer.group_send)(
        f"mailing_{mailing_id}",
        {
            "type": "mailing.finished",
            "total": total
        }
    )


