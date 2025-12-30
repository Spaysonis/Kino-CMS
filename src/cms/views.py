

from .models import Hall
from src.cms.models.page import SeoBlock

from django.shortcuts import render, redirect, get_object_or_404
from src.cms.models.cinema import Cinema
from .forms import MovieForm, SeoBlockForm, NewsForm, UserEditForm, CinemaForm, GalleryFormSet, HallForm
from .models import Gallery
from django.shortcuts import render
from django_tables2 import SingleTableView
from src.user.models import BaseUser
from .tables import UserTable, HallTable



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



        if cinema_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():
            seo = seo_form.save()
            cinema = cinema_form.save(commit=False)
            cinema.seo_block = seo
            cinema.save()
            for image in formset_gallery:
                if image.cleaned_data:
                    gallery = image.save()
                    cinema.gallery.add(gallery)

            hall_seo = SeoBlock.objects.create(
                url='',
                title=f'Seo-{cinema.title}',
                key_words='test',
                description = 'test'

            )

            Hall.objects.create(
                cinema=cinema,
                seo_block=hall_seo,

                number = f'Номер зала 1',
                description='Зал по умолчанию',


            )
            print('все создано успешно')
            return redirect('cinema_list')

    else:
        cinema_form = CinemaForm(prefix='cinema_form')
        seo_form = SeoBlockForm(prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=Gallery.objects.none(), prefix='gallery')


    # hall_table = HallTable(Hall.objects.none())

    context = {
        'cinema_form':cinema_form,
        # 'hall_table': hall_table,
        'seo_form':seo_form,
        'formset_gallery': formset_gallery,




    }
    return render(request, 'cms/cinema_create.html', context)

def cinema_update(request, pk):

    cinema = get_object_or_404(Cinema, pk=pk)
    gallery_qs = Gallery.objects.filter(cinema=cinema)

    if request.method == 'POST':


        cinema_form = CinemaForm(request.POST, request.FILES, instance=cinema, prefix='cinema_form')
        seo_form = SeoBlockForm(request.POST,  instance=cinema.seo_block, prefix='seo_form')
        gallery_form_set = GalleryFormSet(request.POST, request.FILES, queryset=gallery_qs, prefix='gallery')





        if cinema_form.is_valid() and seo_form.is_valid() and gallery_form_set.is_valid():
            print("FILES keys:", list(request.FILES.keys()))



            cinema_form.save()
            seo_form.save()
            instances=gallery_form_set.save()
            cinema.gallery.add(*instances)
            return redirect('cinema_list')

    else:
        cinema_form = CinemaForm(instance=cinema, prefix='cinema_form')
        seo_form = SeoBlockForm(instance=cinema.seo_block, prefix='seo_form')
        gallery_form_set = GalleryFormSet(queryset=gallery_qs, prefix='gallery')


    hall_table = HallTable(Hall.objects.filter(cinema=cinema))
    context = {
        'cinema_form': cinema_form,
        'seo_form': seo_form,
        'hall_table': hall_table,
        'formset_gallery':gallery_form_set,
        'cinema':cinema
    }
    return render(request, 'cms/cinema_update.html', context=context)



def cinema_delete(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)

    if request.method == 'POST':
        cinema.delete()
        return redirect('cinema_list')
    return render(request, 'cms/cinemas.html')





def hall_create(request,pk):
    cinema = get_object_or_404(Cinema, pk=pk)

    if request.method=='POST':



        hall_form = HallForm(request.POST,  request.FILES , prefix='hall_form')

        formset_gallery = GalleryFormSet(request.POST, request.FILES,
                                         queryset=Gallery.objects.none(),
                                         prefix='gallery')

        seo_form = SeoBlockForm(request.POST, prefix='seo_form')

        print('error hal', hall_form.errors)
        print('error seo', seo_form.errors)
        print('error gallery', formset_gallery.errors)

        if hall_form.is_valid()  and seo_form.is_valid() and formset_gallery.is_valid():
            print('not error')
            hall = hall_form.save(commit=False) # 1 тут я сохрнил киношку в памяти (озу)
            hall.cinema = cinema # тут я обратился к киношке (могу обраться ведь у нее уже есть ид)
            # и в поле синема я положил зал(ведь форма уже пройдена)
            seo = seo_form.save() # тут я сохраняю данные из сеоблока ( ведь форма уже пройдена )
            hall.seo_block = seo  # тут я сохрняю в поле сеобок зала данные
            hall.save() # сохраняю зал в память без галеереии

            gallery_objects = formset_gallery.save()  # сохраняю картинки если есть в память
            hall.gallery.set(gallery_objects) # тут у зала появляються связи с картинками, знает пути

            print('end not error')
            return redirect('cinema_list')

    else:
        hall_form = HallForm(prefix='hall_form')
        seo_form = SeoBlockForm(prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=Gallery.objects.none(), prefix='gallery')



    context = {
        'hall_form':hall_form,
        'cinema':cinema,
        'seo_form':seo_form,
        'formset_gallery':formset_gallery
    }

    return render(request,'cms/hall_create.html',context=context)




def hall_update(request, cinema_pk, hall_pk):
    hall = get_object_or_404(Hall, pk=hall_pk, cinema_id=cinema_pk)
    gallery_qs = Gallery.objects.filter(hall=hall)

    # print('object:',hall.number)
    # print('object_cinema:',hall.cinema.title)
    # print('object_s:',hall.seo_block)

    if request.method == 'POST':
        hall_form = HallForm(request.POST, request.FILES, instance=hall, prefix='hall_form')
        seo_form = SeoBlockForm(request.POST, instance=hall.seo_block, prefix='seo_form')
        gallery_form_set = GalleryFormSet(request.POST, request.FILES, queryset=gallery_qs, prefix='gallery')

        if hall_form.is_valid() and seo_form.is_valid() and gallery_form_set.is_valid():
            hall_form.save()
            seo_form.save()
            instances = gallery_form_set.save()
            hall.gallery.add(*instances)
            return redirect('cinema_update', pk=cinema_pk)








    hall_form = HallForm(instance=hall, prefix='hall_form')
    seo_form = SeoBlockForm(instance=hall.seo_block ,prefix='seo_form')
    gallery_formset = GalleryFormSet(queryset=gallery_qs, prefix='gallery')


    context = {
        'hall_form':hall_form,
        'seo_form':seo_form,
        'formset_gallery':gallery_formset,
        'cinema':hall.cinema

    }
    return render(request, 'cms/hall_update.html', context)





def hall_delete(request, cinema_pk, hall_pk):

    hall = get_object_or_404(Hall, pk=hall_pk, cinema_id=cinema_pk)
    hall.delete()
    print('удален ')
    return redirect('cinema_update', pk=cinema_pk)









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

