
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
import json
from .models import  MailTemplate
from django.core.cache import cache
from src.cms.tasks import send_mailing
from celery.result import AsyncResult
from src.user.models import BaseUser
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

def active_mailing(request):
    """
    Возвращаб текущий статус рассылки
    """

    mailing_id = cache.get("current_mailing")
    if not mailing_id:
        return JsonResponse({"active": False})

    data = cache.get(f"mailing:{mailing_id}:progress")
    meta = cache.get(f"mailing:{mailing_id}:meta")
    return JsonResponse({
        "active": True,
        "mailing_id": mailing_id,
        "progress": data,
        'meta':meta
    })


@require_POST
def start_mailing(request):
    """
    получаю ид рассылки и передаю его в целеритаску
    :param request:
    :return:
    """
    data = json.loads(request.body)
    mailing_id = data.get("mailing_id")
    task = send_mailing.delay(mailing_id)
    result = AsyncResult(task.id)
    print(result)
    response = {
        "status": 'ok'
    }
    return JsonResponse(response)


def api_user_modal(request):

    users = BaseUser.objects.all()
    return render(request, 'cms/include/modal_users.html', {'users': users})
