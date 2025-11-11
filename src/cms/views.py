from django.shortcuts import render, redirect, get_object_or_404

from src.user.models import BaseUser
from .forms import MovieForm, SeoBlockForm


from .models import Movie


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

def movie_edit(request):
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        seo_form = SeoBlockForm(request.POST)

        if movie_form.is_valid() and seo_form.is_valid():
            seo_block = seo_form.save()
            movie = movie_form.save(commit=False)
            movie.seo_block = seo_block
            movie.save()
            movie_form.save_m2m()
            return redirect('movie_list')
    else:
        movie_form = MovieForm()
        seo_form = SeoBlockForm()

    context = {
        'active_page': 'movie',
        'page_title': 'Создание фильма',
        'form': movie_form,
        'seo_form': seo_form
    }

    return render(request, 'cms/movie.html', context)