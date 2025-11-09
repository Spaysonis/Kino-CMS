from django.shortcuts import render, redirect

from src.user.models import BaseUser

def admin(request):
    return render(request, 'cms/statistics.html', {
        'active_page': 'statistics',
        'page_title': 'Admin страница'
    })



def users(request):
    return render(request, 'cms/users.html',{
                'active_page':'users',
                'page_title':'Список пользователей'}
    )


def get_user_info(request):
    users = BaseUser.objects.all()
    context = {
        "users": users,
        "active_page": "users"  # ← добавь это!
    }
    return render(request, 'cms/users.html', context)



def news(request):

    context = {
        'active_page':'news',
        'page_title':'Новости'

    }
    return render(request, 'cms/news.html', context)