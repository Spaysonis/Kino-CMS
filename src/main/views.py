from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SimpleRegistrationForm, ProfileEditForm

from src.cms.models.banners import HomePageBanner, BackgroundBanner
from ..cms.models import Cinema, Movie


def movies(request):
    movie = Movie.objects.all()

    context = {
        'movie':movie

    }
    return render(request,'movie', context)


def cinema_list1(request):
    print('вызвавла вью')
    cinema = Cinema.objects.all()
    context ={
        'cinema':cinema
    }
    return render(request, 'main/cinema.html', context)



def user_login(request):
    if request.method == 'POST':
        username = request.POST['login_name']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # На главную после входа
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'main/login.html')




def edit_profile_view(request):

    if request.method == 'POST':


        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()


            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('base_page')
        else:

            messages.error(request, 'Исправьте ошибки в форме!')
    else:
        form = ProfileEditForm(instance=request.user)


    return render(request, 'main/edit_profile.html', {'form': form})




def user_logout(request):
    logout(request)
    return redirect('/')  # Перенаправляет на главную страницу





def user_register(request):

    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('/')
        print(form.errors)
    else:
        form = SimpleRegistrationForm()

    print('error')
    return render(request, 'main/pages/main.html', {'form': form, 'show_register': True,

                                                    })






def main(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies

    }

    return render(request, 'main/pages/main.html', context)



