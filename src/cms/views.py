

from .models import Hall
from src.cms.tables import HallTabel
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string
from src.cms.models.cinema import Cinema

from .forms import MovieForm, SeoBlockForm, NewsForm, UserEditForm, CinemaForm, GalleryFormSet
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



# def upload_gallery_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         img = Gallery.objects.create(image=request.FILES['image'])
#         return JsonResponse({'id':img.id, 'url':img.image.url})
#     return JsonResponse({'error':'error!'}, status=400)



def cinema_list(request):
    cinemas = Cinema.objects.all() # все кинотеатры
    context = {
        'cinemas':cinemas
    }
    return  render(request, 'cms/cinemas.html', context=context)



def cinema_create(request):

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES, prefix='cinema_form')
        seo_form = SeoBlockForm(request.POST, prefix='seo_form')
        formset_gallery = GalleryFormSet(request.POST, request.FILES, queryset=Gallery.objects.none(), prefix='gallery')

        action = request.POST.get('action') # Состояние черновика

        # seo_formset = SeoBlockFormSet(request.POST, instance=cinema)

        #
        # print('cinema' , cinema_form.errors)
        # print('Cinema  valid:', cinema_form.is_valid())
        # print('SEO  valid:', seo_form.is_valid())
        # print("POST данные:", request.POST)
        # print("Cinema title ", request.POST.get('title'))
        # print('*'* 8)
        # print("SEO title ", request.POST.get('title'))


        if cinema_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():
            # print("Cinema title to save:", cinema_form.cleaned_data['title'])
            # print("SEO title to save:", seo_form.cleaned_data['title'])
            seo = seo_form.save()
            cinema = cinema_form.save(commit=False)
            cinema.seo_block = seo
            cinema.is_draft = True
            cinema.save()
            for image in formset_gallery:
                if image.cleaned_data:
                    gallery = image.save()
                    cinema.gallery.add(gallery)
            if action == 'add_hall':
                return redirect('hall_create', cinema_id=cinema.id)
            return redirect('cinema_edit', name='cinema_edit')


    else:
        cinema_form = CinemaForm(prefix='cinema_form')
        seo_form = SeoBlockForm(prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=Gallery.objects.none(), prefix='gallery')

    hall_table = HallTabel(Hall.objects.none())

    context = {
        'cinema_form':cinema_form,
        'hall_table':hall_table,
        'seo_form':seo_form,
        'formset_gallery': formset_gallery,


    }
    return render(request, 'cms/cinema_create.html', context)


def cinema_edit(request, cinema_id):
    cinema = get_object_or_404(Cinema, id=cinema_id) # я получаю синема и его ид на вход
    if request.method == 'POST':
        cinema_form = CinemaForm(
            request.POST,
            request.FILES,
            instance=cinema,
            prefix='cinema_form'

        )

        action = request.POST.get('action')

        seo_form = SeoBlockForm(
            request.POST,
            instance=cinema.seo_block,
            prefix='seo_form'
        )
        if cinema_form.is_valid() and seo_form.is_valid():
            seo_form.save()
            cinema_form.save()
            return redirect('cinema_list')

        cinema_form = CinemaForm(
            instance=cinema,
            prefix='cinema_form'
        )

        seo_form = SeoBlockForm(
            instance=cinema.seo_block,
            prefix='seo_form'
        )

        context = {
            'cinema_form':cinema_form,
            'seo_form':seo_form,
            'cinemas':cinema

        }
        return render(request,'cms/cinema_create.html', context=context)




def cinema_update(request, pk):

    cinema = get_object_or_404(Cinema, pk=pk)
    gallery_qs = Gallery.objects.filter(cinema=cinema)

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES, instance=cinema, prefix='cinema_form')
        seo_form = SeoBlockForm(request.POST,  instance=cinema.seo_block, prefix='seo_form')
        gallery_form_set = GalleryFormSet(request.POST, request.FILES, queryset=gallery_qs)


        if cinema_form.is_valid() and seo_form.is_valid() and gallery_form_set.is_valid():
            cinema_form.save()
            seo_form.save()
            gallery_form_set.save()
            return redirect('cinema_list')

    else:
        cinema_form = CinemaForm(instance=cinema, prefix='cinema_form')
        seo_form = SeoBlockForm(instance=cinema.seo_block, prefix='seo_form')
        gallery_form_set = GalleryFormSet(queryset=gallery_qs)

    hall_table = HallTabel(Hall.objects.filter(cinema=cinema))
    context = {
        'cinema_form': cinema_form,
        'seo_form': seo_form,
        'hall_table': hall_table,
        'gallery_form_set':gallery_form_set
    }
    return render(request, 'cms/cinema_update.html', context=context)



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

