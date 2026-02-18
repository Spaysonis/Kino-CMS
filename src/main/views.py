from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SimpleRegistrationForm, ProfileEditForm
from .models import Schedule

from ..cms.models import Cinema, Movie



def main(request):
    from datetime import date

    movies = Movie.objects.all()
    today = date.today()
    current_movies = Movie.objects.filter(start_date__lte=today, end_date__gte=today).order_by('start_date')

    # start_date > today
    upcoming_movies = Movie.objects.filter(start_date__gt=today).order_by('start_date')


    context = {
        'movies': movies,
        'current_movies':current_movies,
        'upcoming_movies':upcoming_movies

    }
    return render(request, 'main/pages/main.html', context)





def movie_detail(request, pk):
    movie = get_object_or_404(Movie, id=pk)
    cinemas = Cinema.objects.all()
    context = {
        'movie':movie,
        'cinemas':cinemas,

        "rental_days": movie.rental_days()

    }
    return render(request,'main/pages/movie_detail.html', context)


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





