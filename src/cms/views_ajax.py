

"""JsonResponse - Возвращает данные клиенту в Джсон формате """
from django.http import JsonResponse


""" Декоратор require_POST - гарантирует что вью функция будет вызываться только при HTTP запросе с методом ПОСТ"""
from django.views.decorators.http import require_POST

""" Функция get_object_or_404 - ищет обьект модели по указаным параметрам, если обьекта нет, возвращает искулючение Http404  """
from django.shortcuts import get_object_or_404

from src.cms.models.cinema import Cinema


@require_POST
def delete_cinema_image(request, pk, field):
    """
    1) тут я получаю обьект кинотеатра
    2) Получают филд (изображение) кинотеатра через функуцию getattr
    3) если есть имадж я удаляю его, но не сохраняб
    4) через setattr я передаю в него Киношку , поле и значение None- то есть оно становиться пустое
    5) я хохраняю киношку в ктором поле имейдж будет None и возвращаю джсон ответ
    """
    cinema = get_object_or_404(Cinema, pk=pk) # Получаю обьект кинотеатра


    image_field = getattr(cinema, field, None)

    if image_field:
        image_field.delete(save=False)
        setattr(cinema, field, None)
        cinema.save(update_fields=[field])
    return JsonResponse({'status':'ok'})



@require_POST
def upload_cinema_image(request, pk, field):
    """
    1) получаю файил
    2) получаю старое изображение если оно есть то удаляю его
    3) через setattr я обращаюсь к киношке передаю ему поле и фаил для этого поля
    4) сохраняю киношку с новым изображением и возвращаю джсон ответ c путем для сохраненного файла

    """
    print('upload_cinema_image')

    cinema = get_object_or_404(Cinema, pk=pk)

    file = request.FILES.get('file')  # get('file') ищет на фронте фаил с ключем фаил

    if not file:
        return JsonResponse({'error':'no file'}, status=400)

    old_image = getattr(cinema, field)

    if old_image:
        old_image.delete(save=False)

    setattr(cinema, field, file)
    cinema.save(update_fields=[field])
    return JsonResponse({'status':'ok',
                         'url':getattr(cinema, field).url})





