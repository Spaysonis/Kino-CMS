# src/main/tasks.py
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import  get_channel_layer
from django.core.mail import send_mail
from .models import MailTemplate
from src.user.models import BaseUser
from django.core.cache import cache



@shared_task
def send_mailing(mailing_id, users):


    if users == 'all':
        recipients = BaseUser.objects.exclude(email='').values_list('email', flat=True)  # Take user(email) with db
    else:
        recipients = BaseUser.objects.filter(id__in=users).exclude(email='').values_list('email', flat=True)

    cache.set("current_mailing", mailing_id) # state now
    subject = "Тема"
    template = MailTemplate.objects.get(pk=mailing_id) # Take template with db
    html_message = template.file.file.read().decode('utf-8')
    template_name = template.file.name
    total_user = len(recipients)

    progress_key = f"mailing:{mailing_id}:progress"
    meta_key = f"mailing:{mailing_id}:meta"

    # meta data
    cache.set(meta_key, {
        "template_name": template_name,

    })

    # start state data
    cache.set(progress_key, {
        "sent": 0,
        "total_user": total_user,
        "status": "running"
    })

    channel_layer = get_channel_layer()
    sent = 0
    errors= 0
    for i, email in enumerate(recipients, start=1):
        try:
            send_mail(
                subject=subject,
                message='',
                from_email=None,
                recipient_list=[email],
                html_message=html_message
            )
            sent += 1
        except Exception as e:
            errors += 1
            async_to_sync(channel_layer.group_send)(
                f"mailing_{mailing_id}",
                {
                    "type": "mailing.error",
                    "email": email,
                    "error": str(e)
                }
            )
            continue


        cache.set(progress_key, {
            "sent": i,
            "total_user": total_user,
            "status": "running",
        })

        async_to_sync(channel_layer.group_send)(
            f"mailing_{mailing_id}",
            {
                "type": "mailing.progress",
                "progress": int(i / total_user * 100),
                "sent": i,
                "total_user": total_user,
                "email": email
            }
        )


    cache.set(f"mailing:{mailing_id}:progress", {
        "sent":sent ,
        "total_user": total_user,
        "status": "finished"
    })
    cache.delete("current_mailing")



    async_to_sync(channel_layer.group_send)(
        f"mailing_{mailing_id}",
        {
            "type": "mailing.finished",
            "sent": sent
        }
    )


