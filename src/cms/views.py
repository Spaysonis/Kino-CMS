from .models import Hall
from src.cms.tables import HallTabel
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404


from src.cms.models.cinema import Cinema

from .forms import MovieForm, SeoBlockForm, NewsForm, UserEditForm, CinemaForm
from .models import Gallery

from django.views.generic import ListView

from django.shortcuts import render
from django_tables2 import SingleTableView
from src.user.models import BaseUser

from .tables import UserTable

def admin(request):
    return render(request, 'cms/statistics.html', {
        'active_page': 'statistics',
        'page_title': 'Admin страница'
    })



# def users(request):
#     table = UserTable(BaseUser.objects.all())
#     RequestConfig(request, paginate={"per_page": 20}).configure(table)  # пагинация по 20
#     return render(request, "users/users.html", {"table": table})



def upload_gallery_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = Gallery.objects.create(image=request.FILES['image'])
        return JsonResponse({'id':img.id, 'url':img.image.url})
    return JsonResponse({'error':'error!'}, status=400)



def cinema_list(request):
    cinemas = Cinema.objects.all() # все кинотеатры
    context = {
        'cinemas':cinemas
    }
    return  render(request, 'cms/cinemas.html', context=context)



def cinema_create(request, pk=None):

    if pk:
        cinema = get_object_or_404(Cinema, pk=pk)
    else:
        cinema = None


    if request.method == 'POST':
        form = CinemaForm(request.POST, request.FILES, instance=cinema)
        print(form.errors)
        if form.is_valid():
            form.save()

            print('=')
        return redirect('cinema_list')

    else:
        form = CinemaForm(instance=cinema)

    table = HallTabel(Hall.objects.all())
    context = {
        'form':form,
        'cinema':cinema,
        'image_num': [1,2,3,4,5],
        'hall_table': table,
    }
    return render(request, 'cms/cinema_create.html', context)


def cinema_delete(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)

    if request.method == 'POST':
        cinema.delete()
        return redirect('cinema_list')
    return render(request, 'cms/cinemas.html')







def news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        print(request.POST)  # ← вот здесь мы смотрим всё, что отправляет браузер
        if form.is_valid():
            print(form.cleaned_data['is_active'])  # True или False
    else:
        form = NewsForm()

    context = {
        'active_page': 'news',
        'page_title': 'Новости',
        'form': form
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



def edit_user(request, pk):

    user = get_object_or_404(BaseUser, pk=pk) # найти в бд(BaseUser)  юзера по такому ключу

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'cms/edit_user.html', {'form':form,
                                                  'user': user})




class UserListView(SingleTableView):
    model = BaseUser
    table_class = UserTable
    template_name = 'cms/users.html'
    paginate_by = 6
    SingleTableView.table_pagination = False



def test(request):
    return render(request, 'cms/test.html')

