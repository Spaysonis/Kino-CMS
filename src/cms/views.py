from zipimport import alt_path_sep

from .models import Hall, Slider, HomePageBanner
from src.cms.models.page import SeoBlock, Updates
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from src.cms.models.cinema import Cinema
from .forms import MovieForm, SeoBlockForm, UpdatesForm, UserEditForm, CinemaForm, GalleryFormSet, HallForm,  HomePageBannerForm, SliderFormSet
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

def create(request):

    if request.method == 'GET':
        banners = []

        for banner_type, cfg in BANNER_CONFIG.items():
            banner = HomePageBanner.objects.filter(type_banner=banner_type).first()

            form = HomePageBannerForm(instance=banner, prefix=cfg['form_prefix'])
            formset = SliderFormSet(queryset=banner.slider.all() if banner else Slider.objects.none(), prefix=cfg['formset_prefix'])

            banners.append({
                "type":banner_type,
                'form':form,
                'formset':formset
            })





def create_banners(request):

    if request.method == 'GET':
        for banner_type, cfg in BANNER_CONFIG.items():
            # banner = HomePageBanner.objects.filter(
            #     type_banner=banner_type).first()
            print("----------,",cfg)


    top_banner = HomePageBanner.objects.filter(type_banner=HomePageBanner.TOP_BANNER).first()
    news_banner = HomePageBanner.objects.filter(type_banner=HomePageBanner.NEWS_BANNER).first()


    print(top_banner, '---top_banner')
    print(news_banner, '---news_banner')
    if top_banner:
        print('tp',top_banner.type_banner)
    if news_banner:
        print('nb',news_banner.type_banner)


    top_banner_form = HomePageBannerForm(instance=top_banner, prefix='top_banner_form')
    top_banner_formset = SliderFormSet(queryset=top_banner.slider.all() if top_banner else Slider.objects.none(), prefix='top_banner_formset')

    news_banner_form = HomePageBannerForm(instance=news_banner, prefix='news_banner_form')
    news_banner_formset = SliderFormSet(queryset=news_banner.slider.all() if news_banner else Slider.objects.none(), prefix='news_banner_formset')



    if request.method == 'POST':

        pprint(dict(request.POST))
        banner_type = request.POST.get('banner_type')
        print(banner_type)
        print()
        if banner_type == 'TB':
            top_banner_form = HomePageBannerForm(request.POST, request.FILES,prefix='top_banner_form' )
            top_banner_formset = SliderFormSet(request.POST,
                                               request.FILES,
                                               queryset=top_banner.slider.all() if top_banner else Slider.objects.none(),
                                               prefix='top_banner_formset')
            if top_banner_form.is_valid() and top_banner_formset.is_valid():
                banner, created = HomePageBanner.objects.update_or_create(
                    type_banner=banner_type,
                    defaults= {
                        'is_active':top_banner_form.cleaned_data['is_active'],
                        'speed':top_banner_form.cleaned_data['speed']

                    }
                )

                slides = top_banner_formset.save(commit=False)
                for obj in top_banner_formset.deleted_objects:
                    obj.delete()

                for slide in slides:
                    slide.save()
                banner.slider.set(
                    list(banner.slider.all()) + slides
                )

                return JsonResponse({
                    'success': True,
                    'banner_id': banner.id,
                    'created': created
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'form': top_banner_form.errors,
                        'formset': top_banner_formset.errors
                    }
                })

        elif banner_type == 'NB':
            pass

    else:

        context = {
            'top_banner_form':top_banner_form,
            'news_banner_form':news_banner_form,

            'top_banner_formset':top_banner_formset,
            'news_banner_formset':news_banner_formset
        }

        return render(request, 'cms/banners.html', context)



# def update_form(request, content_type_slug,pk=None):
#     print('fun create  enter CONTENT TYPE SLUG', content_type_slug) # # NEWS
#     print('pk----',pk)
#     content_type = Updates.ContentType.from_slug(content_type_slug)
#     print(content_type)
#
#     instance = None # сущьность акции или новости
#     # formset_gallery = GalleryFormSet(queryset=Gallery.objects.none())
#
#
#     if pk:
#
#         instance = get_object_or_404(Updates, pk=pk, content_type=content_type)
#         gallery_queryset = instance.gallery.all()
#     else:
#         gallery_queryset = Gallery.objects.none()
#
#
#     if request.method == 'POST':
#
#         update = UpdatesForm(request.POST, request.FILES, instance=instance , prefix='update')
#         seo_form = SeoBlockForm(request.POST, instance=instance.seo_block if instance else  None,prefix='seo_form')
#         formset_gallery = GalleryFormSet(request.POST, request.FILES, queryset=gallery_queryset, prefix='gallery')
#
#         if update.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():
#             obj = update.save(commit=False)
#             obj.content_type = content_type
#             seo_block = seo_form.save()
#             obj.seo_block = seo_block
#             obj.save()
#
#             gallery_objects = formset_gallery.save()  # сохраняю картинки если есть в память
#             obj.gallery.set(gallery_objects)
#             print('also saving fun create return content type ', content_type)
#             return redirect(f'/admin/content/?type={content_type_slug}')
#         else:
#
#             print(update.errors)
#             print(seo_form.errors)
#             print(formset_gallery.errors)
#
#
#             return render(request, 'cms/content_create.html', {
#                 'update': update,
#                 'seo_form': seo_form,
#                 'formset_gallery': formset_gallery,
#                 'content_type': content_type_slug,
#             })
#
#
#
#     else:
#         update = UpdatesForm(instance=instance if pk else None, prefix='update')
#         seo_form = SeoBlockForm(instance=instance.seo_block if pk else None,prefix='seo_form')
#         formset_gallery = GalleryFormSet(queryset=gallery_queryset, prefix='gallery')
#         context = {
#                 'update':update,
#                 'content_type':content_type_slug,
#                 'seo_form':seo_form,
#                 'formset_gallery':formset_gallery
#                 # 'seo_form':seo_form,
#                 # 'formset_gallery':formset_gallery
#
#             }
#         return render(request, 'cms/content_create.html', context)
#
#
#












#
# def create_update(request, content_type):
#
#     template = content_type.lower()
#
#     if request.method == 'POST':
#         update_form = UpdatesForm(request.POST, request.FILES, prefix='update_form')
#         seo_form = SeoBlockForm(request.POST, prefix='seo_form')
#         formset_gallery = GalleryFormSet(request.POST,request.FILES,
#                                          queryset=Gallery.objects.none(), prefix='gallery')
#
#         if update_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():
#
#             update = update_form.save(commit=False)
#             update.content_type = content_type
#             seo = seo_form.save()
#             update.seo_block = seo
#             update.save()
#             gallery_objects = formset_gallery.save()
#             update.gallery.set(gallery_objects)
#             return redirect(template)
#     else:
#         update_form = UpdatesForm(prefix='update_form')
#         seo_form = SeoBlockForm(prefix='seo_form')
#         formset_gallery = GalleryFormSet(queryset=Gallery.objects.none(), prefix='gallery')
#
#     context = {
#         'update_form':update_form,
#         'seo_form':seo_form,
#         'formset_gallery':formset_gallery
#     }
#     print('template',template)
#     return render(request,f'cms/{template+'_create'}.html', context)
#


#
# def news_update(request):
#     return
#




# def update_form(request, content_type, pk=None):
#
#     publication = None
#     gallery_qs = Gallery.objects.none()
#     print('PK:', pk)
#
#     if pk:
#         print('get pk key')
#         publication = get_object_or_404(Updates, pk=pk, content_type=content_type)
#         gallery_qs = publication.gallery.all()
#
#         print('instance', publication.main_image)
#         print('gallery qs',gallery_qs)
#
#     if request.method == "POST":
#         print('POST')
#         publication_form = UpdatesForm(request.POST, request.FILES, instance=publication,prefix='news_form')
#
#         seo_form = SeoBlockForm(request.POST, instance=publication.seo_block if publication else None, prefix='seo_form')
#
#         formset_gallery = GalleryFormSet(request.POST, request.FILES,
#                                          queryset=gallery_qs,
#                                          prefix='gallery')
#
#         print('news_form error', publication_form.errors)
#         print('news_form error', publication_form.errors)
#         print('seo_form error', seo_form.errors)
#         print('formset_gallery error', formset_gallery.errors)
#
#
#
#
#         if publication_form.is_valid() and seo_form.is_valid() and formset_gallery.is_valid():
#
#             update = publication_form.save(commit=False)
#             update.content_type = content_type
#
#
#             seo_block = seo_form.save()
#             update.seo_block = seo_block
#             update.save()
#             gallery_objects = formset_gallery.save()
#             update.gallery.set(gallery_objects)
#             print('save done')
#             return redirect('news')
#
#     else:
#
#         publication_form = UpdatesForm(instance=publication , prefix='news_form')
#         seo_form = SeoBlockForm(instance=publication.seo_block if publication else None ,prefix='seo_form')
#         formset_gallery = GalleryFormSet(queryset=gallery_qs, prefix='gallery')
#
#     context = {
#         'publication_form':publication_form,
#         'seo_form':seo_form,
#         'formset_gallery':formset_gallery,
#
#
#     }
#     print('pk-------',publication_form.instance.pk)
#     return render(request, 'cms/news_update.html', context)
#
#


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





