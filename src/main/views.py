from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SimpleRegistrationForm, ProfileEditForm
from src.cms.models.cinema import Movie
from ..cms.models import Cinema


def cinema_list1(request):
    print('вызвавла вью')
    cinema = Cinema.objects.all()
    context ={
        'cinema':cinema
    }
    return render(request, 'main/cinema.html', context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # На главную после входа
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'main/login.html')


def register_view(request):
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('/')
    else:
        form = SimpleRegistrationForm()

    return render(request, 'main/register.html', {'form': form})


def edit_profile_view(request):
    """РЕДАКТИРОВАНИЕ ПРОФИЛЯ"""
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




def logout_view(request):
    logout(request)
    return redirect('/')  # Перенаправляет на главную страницу

def main_page(request):

    movie = Movie.objects.all()



    return render(request, 'main/main_view.html', {
        'active_page':'main_page',
        'page_title':'Главная страница',
        'films': movie
    })



