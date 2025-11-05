from django.shortcuts import render, redirect
from .models import Slider, NewsPromoBanner
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SimpleRegistrationForm, ProfileEditForm


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

    return render(request, 'cms/login.html')


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

    return render(request, 'cms/register.html', {'form': form})





def edit_profile_view(request):
    """РЕДАКТИРОВАНИЕ ПРОФИЛЯ"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('/edit_profile')
    else:
        print(
            'error'
        )
        form = ProfileEditForm(instance=request.user)
    return render(request, 'cms/edit_profile.html', {'form': form})




def main_page(request):
    return render(request, 'cms/main_page.html', {
        'active_page':'base_page',
        'page_title':'Главная страница'
    })


def logout_view(request):
    logout(request)
    return redirect('/')  # Перенаправляет на главную страницу



