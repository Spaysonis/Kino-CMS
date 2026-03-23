from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SimpleRegistrationForm, ProfileEditForm
from .models import Schedule, Booking, Visitor

from ..cms.models import Cinema, Movie, Hall, Page
from src.main.utils import get_device_type, get_country_from_ip, get_client_ip
from datetime import date
from django.utils import timezone


def cinema(request):

    cinemas = Cinema.objects.all()

    context = {
        'cinemas':cinemas
    }
    return render(request, 'main/pages/cinemas.html',context)


def cinema_card(request):
    from datetime import date
    cinema_id = request.GET.get('id')
    cinema_obj = get_object_or_404(Cinema, id=cinema_id)
    hall_obj = Hall.objects.filter(cinema=cinema_obj)


    schedule_obj = Schedule.objects.filter(hall__cinema=cinema_obj, date=date.today())

    active_pages = Page.active_pages()

    print(hall_obj)
    print(schedule_obj)

    context = {
        'cinema':cinema_obj,
        'hall_obj':hall_obj,
        'schedule_obj':schedule_obj,
        'active_pages':active_pages
    }
    return render(request, 'main/pages/cinema_card.html', context)



def schedule(request):
    cinemas = Cinema.objects.all()
    movies = Movie.objects.all()
    halls = Hall.objects.all()

    schedules = Schedule.objects.all()

    # получаем параметры
    cinema_id = request.GET.get('cinema')
    movie_id = request.GET.get('movie')
    hall_id = request.GET.get('hall')
    date_str = request.GET.get('date_session')
    selected_date = date_str if date_str else timezone.localdate().strftime("%Y-%m-%d")
    print(selected_date)

    try:
        selected_cinema = int(cinema_id) if cinema_id else None
    except ValueError:
        selected_cinema = None

    try:
        selected_movie = int(movie_id) if movie_id else None
    except ValueError:
        selected_movie = None

    try:
        selected_hall = int(hall_id) if hall_id else None
    except ValueError:
        selected_hall = None



    # фильтры
    if cinema_id:
        schedules = schedules.filter(hall__cinema_id=cinema_id)

    if movie_id:
        schedules = schedules.filter(movie_id=movie_id)

    if hall_id:
        schedules = schedules.filter(hall_id=hall_id)

    if date_str:
        schedules = schedules.filter(date=selected_date)
    else:
        schedules = schedules.filter(date=timezone.localdate())  # по умолчанию сегодня

    context = {
        'cinemas': cinemas,
        'movies': movies,
        'halls': halls,
        'schedules': schedules,
        'selected_cinema': selected_cinema,
        'selected_movie': selected_movie,
        'selected_hall': selected_hall,
        'selected_date':selected_date

    }

    return render(request, 'main/pages/schedule.html', context)



def poster_coming(request):
    movies = Movie.objects.all()

    today = date.today()
    current_movies = Movie.objects.filter(start_date__lte=today, end_date__gte=today).order_by('start_date')

    context = {
        'current_movies':movies
    }
    return render(request, 'main/pages/poster.html', context)



def main(request):


    movies = Movie.objects.all()
    today = date.today()
    current_movies = Movie.objects.filter(start_date__lte=today, end_date__gte=today).order_by('start_date')

    # start_date > today
    upcoming_movies = Movie.objects.filter(start_date__gt=today).order_by('start_date')


    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    ip = get_client_ip(request)
    device = get_device_type(request)
    country = get_country_from_ip(ip)

    visitor, created = Visitor.objects.get_or_create(
        session_key=session_key,
        defaults={
            'device_type': device,
            'ip_address': ip,
            'country': country,
        }
    )

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






def booking(request, pk):
    user = request.user

    if request.method == 'POST':
        if not user.is_authenticated:
            return redirect('/')



        user = request.user
        print(user)
        print('POST')
        session_id = request.POST.get('session_id')
        selected_seats = request.POST.get('selected_seats')
        selected_type = request.POST.get('action')
        print(session_id)
        print(selected_seats)
        print(selected_type)



    id_session = Schedule.objects.get(pk=pk)
    movie = id_session.movie


    print(id_session.hall.gallery)
    taken_seats = Booking.objects.filter(
        schedule=id_session
    ).values_list('row', 'place')

    context = {
        'id_session':id_session,
        'movie':movie,
        "format_movie":id_session.format,
        "hall":id_session.hall,
        'session':id_session,
        'first_row':range(1,13),
        'second_row':range(1,11),
        'vip_row':range(1,19),
        'taken_seats': list(taken_seats)
    }
    return render(request, 'main/pages/booking.html', context=context)






def cinema_list1(request):
    print('вызвавла вью')
    cinema = Cinema.objects.all()
    context ={
        'cinema':cinema
    }
    return render(request, 'main/cinemas.html', context)



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





