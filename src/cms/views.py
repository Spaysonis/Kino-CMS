from django.forms import formset_factory

from .models import Hall, Slider, HomePageBanner, BackgroundBanner
from src.cms.models.page import SeoBlock, Updates
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from src.cms.models.cinema import Cinema, Movie
from .forms import MovieForm, SeoBlockForm, UpdatesForm, UserEditForm, CinemaForm, GalleryFormSet, HallForm, \
    HomePageBannerForm, SliderFormSet, BackgroundBannerForm
from .models import Gallery
from django.shortcuts import render
from django_tables2 import SingleTableView
from src.user.models import BaseUser
from .tables import UserTable, HallTable, UpdatesTable



def admin(request):
    return render(request, 'cms/statistics.html', {
        'active_page': 'statistics',
        'page_title': 'Admin страница'
    })



def movies(request):
    from datetime import date
    '''
    exact - Равно (по умолчанию, если lookup не указан)
    gt - больше
    gte - больше или равно
    lt - меньше
    lte - меньше или равно
    '''


    today = date.today()

    # start_date <= today; end_date >= today
    current_movies = Movie.objects.filter(start_date__lte=today, end_date__gte=today).order_by('start_date')

    # start_date > today
    upcoming_movies = Movie.objects.filter(start_date__gt=today).order_by('start_date')

    movie = Movie.objects.all().count()


    context = {
        'active_page': 'movie_list',
        'current_movies':current_movies,
        'upcoming_movies':upcoming_movies,
        'movies':movie

    }
    return render(request, 'cms/movies.html', context=context)



def movie_create_or_update(request, pk=None):
    movie = get_object_or_404(Movie, pk=pk) if pk else None

    gallery_qs = movie.gallery.all() if movie else Gallery.objects.none()


    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES, instance=movie, prefix='movie_form')
        seo_form = SeoBlockForm(request.POST, instance=movie.seo_block if movie else None, prefix='seo_form')
        formset_gallery = GalleryFormSet(request.POST, request.FILES, queryset=gallery_qs, prefix='gallery')

        if movie_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():

            seo_block = seo_form.save()
            movie = movie_form.save(commit=False)
            movie.seo_block = seo_block
            movie.save()
            movie_form.save_m2m()

            gallery_object = formset_gallery.save()
            movie.gallery.add(*gallery_object)
            return redirect('movies')
        else:
            print('movie_form_error^', movie_form.errors,
                  '\nseo_form_errro', seo_form.errors,
                  '\ngformset error', formset_gallery.errors)
    else:
        movie_form = MovieForm(instance=movie, prefix='movie_form')
        seo_form = SeoBlockForm(instance=movie.seo_block if movie else None, prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=gallery_qs, prefix='gallery')



    context = {
        'movie_form':movie_form,
        'seo_form':seo_form,
        'formset_gallery' :formset_gallery
    }

    return render(request, 'cms/movie_edit.html', context=context)



def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        movie.delete()
        return redirect('movies')
    return render(request, 'cms/movies.html')



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
            gallery_objects = formset_gallery.save()
            cinema.gallery.set(gallery_objects)


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
                is_default = True


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
            print('сработал синема апдейт вместо создать зал')
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
    #gallery_qs = Gallery.objects.filter(hall=hall)
    gallery_qs = hall.gallery.all()

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









def content_list(request):


    slug = request.GET.get('type')
    print("------- QUERY PARAM ----- ", slug) # news
    content_type = Updates.ContentType.from_slug(slug)
    print('-------content_type',content_type) # NEWS
    qs = Updates.objects.all()
    if content_type: # NEWS
            # ЕСЛИ Я ПОУЛЧИЛ КОНТЕНТ ТАЙП АППЕР ТО Я ФИЛЬТУЮ БАЗУ ДАННЫХ С НОВОСТЯМИ ПО КОНТЕНТ ТИПУ, content_type
        qs = qs.filter(content_type=content_type) # NEWS
        print(len(qs))


    table = UpdatesTable(data=qs, content_type=content_type, request=request)

    print('retrun content type', slug)
    return render(
        request,
        'cms/content_list.html',
        {
            'table': table,
            'slug': slug, # news
            # 'active_page': content_type,
            'content_type':content_type
        }
    )




def create_news_or_action(request, slug):

    content_type = Updates.ContentType.from_slug(slug)

    if request.method == 'POST':

        update_form = UpdatesForm(request.POST, request.FILES, prefix='update')
        seo_form = SeoBlockForm(request.POST, prefix='seo_form')
        formset_gallery = GalleryFormSet(request.POST, request.FILES, queryset=Gallery.objects.none(), prefix='gallery')

        if update_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():

            seo_block = seo_form.save()
            update = update_form.save(commit=False)
            update.seo_block = seo_block
            update.content_type = content_type
            update.save()

            gallery_objects = formset_gallery.save()
            update.gallery.set(gallery_objects)

            url = reverse('content_list')
            url += f'?type={slug}'
            return redirect(url)

    else:
        update_form = UpdatesForm(prefix='update')
        seo_form = SeoBlockForm(prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=Gallery.objects.none(), prefix='gallery')

    context = {
        'slug':slug,
        'update':update_form,
        'seo_form':seo_form,
        'formset_gallery':formset_gallery
    }

    return render(request,'cms/content_create.html', context)



def update_news_or_action(request,slug, pk):


    instance = get_object_or_404(Updates, pk=pk)
    gallery_qs = Gallery.objects.filter(updates=instance)


    if request.method == 'POST':
        update_form = UpdatesForm(request.POST, request.FILES,instance=instance, prefix='update')
        seo_form = SeoBlockForm(request.POST, instance=instance.seo_block, prefix='seo_form')
        formset_gallery = GalleryFormSet(request.POST, request.FILES, queryset=gallery_qs, prefix='gallery')

        if update_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():


            update = update_form.save(commit=False)
            seo_block = seo_form.save()
            update.seo_block = seo_block
            update.save()


            gallery_object = formset_gallery.save()
            instance.gallery.set(gallery_object)

            url = reverse('content_list')
            url += f'?type={slug}'
            return redirect(url)


        else:
            print('update_form', update_form.errors)
            print('seo_form',seo_form.errors)
            print('formset_gallery',formset_gallery.errors)



    else:
        update_form = UpdatesForm(instance=instance, prefix='update')
        seo_form = SeoBlockForm(instance=instance.seo_block, prefix='seo_form')
        formset_gallery = GalleryFormSet(queryset=gallery_qs, prefix='gallery')

    context = {
        'update':update_form,
        'seo_form':seo_form,
        'formset_gallery':formset_gallery,
        'slug':slug,
        'instance':instance
    }
    return render(request,'cms/content_create.html', context)



def delete_news_or_action(request, pk):
    instance = get_object_or_404(Updates, pk=pk)
    instance.delete()
    full_url = request.GET.get('full_url', reverse('content_list'))

    return redirect(full_url)





from django.http import JsonResponse


from pprint import pprint

from src.cms.services.banners import BANNER_CONFIG









def create_banners(request):


    if request.method == 'GET':
        banners = []

        for banner_type, cfg in BANNER_CONFIG.items():
            banner = HomePageBanner.objects.filter(type_banner=banner_type).first()

            form = HomePageBannerForm(instance=banner, prefix=cfg['form_prefix'])
            formset = SliderFormSet(queryset=banner.slider.all() if banner else Slider.objects.none(),
                                    prefix=cfg['formset_prefix'])

            banners.append({
                "type": banner_type,
                'form': form,
                'formset': formset
            })


        background_banner = BackgroundBanner.objects.first()
        background_form = BackgroundBannerForm(instance=background_banner)

        return render(request, 'cms/banners.html', {
            'banners': banners,
            'background_form':background_form,
            'background_banner':background_banner

        })


    if request.method == 'POST':



        type_banner = request.POST.get('bannerType') # NB

        banner = HomePageBanner.objects.filter(type_banner=type_banner).first()

        print(banner)


        prefix_form = BANNER_CONFIG[type_banner]['form_prefix']
        prefix_formset = BANNER_CONFIG[type_banner]['formset_prefix']
        print('pre form ------', prefix_form)
        print('pre set ------', prefix_formset)




        form = HomePageBannerForm(request.POST, request.FILES, prefix=prefix_form)
        formset = SliderFormSet(request.POST, request.FILES, prefix=prefix_formset)



        if form.is_valid() and formset.is_valid():

            banner, created = HomePageBanner.objects.update_or_create(
                type_banner=type_banner,
                defaults=form.cleaned_data
            )

            sliders = formset.save(commit=False)

            for obj in formset.deleted_objects:# deleted_objects  смотрит на обьк. которые помечены delete
                obj.delete()


            for slide in sliders:
                slide.save()


            old_slide = []

            for slide in banner.slider.all():
                old_slide.append(slide)

            for slide in sliders:
                old_slide.append(slide)

            banner.slider.set(old_slide)

            return JsonResponse({
                        'success': True,
                        'banner_id': banner.id,
                        'created': created
            })
        return JsonResponse({
            'success': False,
            'banner_id':  banner.id,
            'form_error':form.errors,
            'formset_error':formset.errors
        })



def background_banner(request):
    print('data in views')


    banner = BackgroundBanner.objects.first()



    if request.method == 'POST':
        form = BackgroundBannerForm(request.POST, request.FILES, instance=banner)
        print(form.data)


        if form.is_valid():

            if request.POST.get('delete_image') == 'true':
                if banner.main_image:
                    banner.main_image.delete(save=False)
                banner.main_image = None

            banner = form.save(commit=False)
            if not banner.is_use_image:
                banner.main_image.delete(save=False)
                banner.main_image = None
            banner.save()






            return (
                JsonResponse({
                'success': True,
                    'banner':banner.id,


                }))
        else:
            return JsonResponse({
        'success': False,
        'error':form.errors})






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





