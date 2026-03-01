# src/main/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Mailing
from src.user.models import BaseUser


@shared_task
def send_mailing(mailing_id):
    # Получаем рассылку
    mailing = Mailing.objects.get(id=mailing_id)

    # Получаем ВСЕХ пользователей с email (или только подписанных - как хотите)
    recipients = BaseUser.objects.exclude(email='').values_list('email', flat=True)

    # Отправляем каждому письмо
    for email in recipients:
        send_mail(
            subject=mailing.subject,
            message='',  # Пустой текст
            from_email='machete1445@gmail.com',  # Ваш email
            recipient_list=[email],
            html_message=mailing.content  # HTML содержимое
        )

    # Опционально: меняем статус рассылки
    mailing.status = 'sent'
    mailing.save()