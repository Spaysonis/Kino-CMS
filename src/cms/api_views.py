
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Mailing, MailTemplate
from ..user.models import BaseUser
from src.cms.tasks import send_mailing


def upload_mailing_api(request):
    file = request.FILES['file']
    mailing_temple = MailTemplate.objects.create(file=file)

    all_mailings = MailTemplate.objects.order_by('-created_at')
    if all_mailings.count() > 5:
        mailings_to_delete = all_mailings[5:]
        for m in mailings_to_delete:
            if m.file:
                m.file.delete()
            m.delete()

    return JsonResponse({
        'status': 'ok',
        'filename': mailing_temple.file.name
    })



def delete_mailing_api(request):
    # API для удадления
    return JsonResponse({'status': 'ok'})



@require_POST
def start_mailing(request):

    data = json.loads(request.body)
    mailing_id = data.get("mailing_id")


    if not mailing_id:
        return JsonResponse({"status": "error", "message": "Mailing ID не указан"})

    mail_template = MailTemplate.objects.get(id=mailing_id)
    mailing = Mailing.objects.create(template=mail_template, status="processing")

    # Получаем количество получателей
    total = BaseUser.objects.exclude(email='').count()
    mailing.total_emails = total
    mailing.status = 'processing'
    mailing.sent_emails = 0
    mailing.progress = 0
    mailing.save(update_fields=["total_emails", "status", "sent_emails", "progress"])



    # Запускаем Celery task
    print('send')
    send_mailing.delay(mailing.id)

    return JsonResponse({"status": "ok", "mailing_id": mailing.id})