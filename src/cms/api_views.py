from django.http import JsonResponse
from .models import Mailing




def upload_mailing_api(request):

    # API для загрузки
    print('=' * 50)
    print('API VIEW ВЫЗВАНА!')
    print('Method:', request.method)
    print('GET:', request.GET)
    print('POST:', request.POST)
    print('FILES:', request.FILES)
    print('=' * 50)

    return JsonResponse({'status': 'ok', 'message': 'API work'})



def delete_mailing_api(request):
    # API для удадления
    return JsonResponse({'status': 'ok'})

