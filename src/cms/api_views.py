
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import  MailTemplate
from ..user.models import BaseUser
from src.cms.tasks import send_mailing
from celery.result import AsyncResult

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
    mail_template = MailTemplate.objects.get(id=mailing_id)


    task = send_mailing.delay(mail_template.id)
    result = AsyncResult(task.id)

    response = {
        "status": result.status
    }
    return JsonResponse(response)
