from django.http import JsonResponse
from .models import Mailing




def upload_mailing_api(request):
    file = request.FILES['file']
    mailing = Mailing.objects.create(file=file)

    all_mailings = Mailing.objects.order_by('-created_at')
    if all_mailings.count() > 5:
        mailings_to_delete = all_mailings[5:]
        for m in mailings_to_delete:
            if m.file:
                m.file.delete()
            m.delete()

    return JsonResponse({
        'status': 'ok',
        'filename': mailing.file.name
    })



def delete_mailing_api(request):
    # API для удадления
    return JsonResponse({'status': 'ok'})

