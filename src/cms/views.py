from django.shortcuts import render

from django.contrib.auth.decorators import login_required



def statistics(request):
    return render(request, 'cms/statistics.html', {
        'active_page': 'statistics',
        'page_title': 'Статистика',
    })


def banners(request):
    return render(request, 'cms/banners.html', {
        'active_page': 'banners',
        'page_title': 'Баннеры',
    })

def films(request):
    return render(request, 'cms/films.html',{
        'active_page':'films',
        'page_title':'Фильмы'
    })