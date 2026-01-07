import django_tables2 as tables
from src.user.models import BaseUser
from src.cms.models.cinema import Hall
from src.cms.models.page import Updates


from django.utils.html import mark_safe
from django.urls import reverse

class HallTable(tables.Table):
    number = tables.Column(verbose_name='Название')
    date_create = tables.DateTimeColumn(
        verbose_name='Дата создания',
        format='d.m.Y'
    )
    actions = tables.Column(empty_values=(), verbose_name='', orderable=False,
                            attrs={
                                "td": {"style": "width: 260px;"},
                                "th": {"style": "width: 260px;"}
                            }
                            ) # пустая колонка
    # verbose_name=''- чтоб в шапке колонки  ничего не писалось
    # orderable = False нельзя сортировать по этой колоке
    # empty_values = () всегда будет колонка в шапке даже если нет данных

    class Meta:
        fields = ('number', 'date_create', 'actions')
        orderable = False

        model = Hall
        template_name = "django_tables2/bootstrap4.html"

        attrs = {"class": "table table-bordered table-primary"}

    def render_actions(self, record):
        update_url = reverse('hall_update', args=[record.cinema.pk, record.pk])
        delete_url = reverse('hall_delete', args=[record.cinema.pk, record.pk])

        if record.is_default:
            return mark_safe(
                f'''
                            <div class="d-flex justify-content-between " >
                                <span></span>  <!-- пустой элемент для выравнивания -->
                                <a href="{update_url}" class="btn btn-sm btn-warning" >Редактировать</a>
                            </div>
                            '''
            )
        return mark_safe(
            f'''
                    <div class="d-flex justify-content-between" >
                        <a href="{delete_url}" class="btn btn-sm btn-danger">Удалить</a>
                        <a href="{update_url}" class="btn btn-sm btn-warning">Редактировать</a>
                    </div>
                '''
        )





class UpdatesTable(tables.Table):
    title = tables.Column(verbose_name='Название')
    publication_data = tables.DateTimeColumn(
        verbose_name='Дата создания',
        format='d.m.Y'
    )
    is_active = tables.Column(verbose_name='Статус')
    actions = tables.Column(empty_values=(), verbose_name='', orderable=False,
                            attrs={
                                "td": {"style": "width: 260px;"},
                                "th": {"style": "width: 260px;"}
                            }
                            ) # пустая колонка
    # verbose_name=''- чтоб в шапке колонки  ничего не писалось
    # orderable = False нельзя сортировать по этой колоке
    # empty_values = () всегда будет колонка в шапке даже если нет данных

    def __init__(self, *args, content_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = content_type
        print( 'type content', self.content_type) # NEWS

    class Meta:
        fields = ('title', 'publication_data', 'is_active', 'actions')
        orderable = False

        model = Updates
        template_name = "django_tables2/bootstrap4.html"

        attrs = {"class": "table table-bordered table-primary"}

    def render_actions(self, record):
        full_url = self.request.get_full_path()
        print('next url',full_url)

        update_url = reverse('content_update', args=[Updates.ContentType.to_slug(self.content_type), record.pk])
        delete_url = reverse('delete_update', args=[ record.pk])


        return mark_safe(
            f'''
                    <div class="d-flex justify-content-between" >
                        <a href="{delete_url}?full_url={full_url}" class="btn btn-sm btn-danger">Удалить</a>
                        <a href="{update_url}" class="btn btn-sm btn-warning">Редактировать</a>
                    </div>
                '''
        )




class UserTable(tables.Table):
    id = tables.Column(verbose_name='ID')
    date_joined = tables.DateTimeColumn(verbose_name='Дата регистрации', format='d.m.Y H:i')
    date_of_birth = tables.Column(verbose_name='Дата рождения')
    username = tables.Column(verbose_name='Логин')
    email = tables.Column(verbose_name='Email')
    phone_num = tables.Column(verbose_name='Телефон')
    full_name = tables.Column(verbose_name='ФИО', accessor='first_name')
    nick_name = tables.Column(verbose_name='Псевдоним')
    city = tables.Column(verbose_name='Город')

    edit = tables.TemplateColumn(
        '<a href="{% url "edit_user" record.id %}" class="btn btn-sm btn-primary">Редактировать</a>',
        verbose_name='Действие',
        orderable=False
    )

    class Meta:
        model = BaseUser
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "date_joined", "date_of_birth", "username", "email",
                  "phone_num", "full_name", "nick_name", "city", "edit")
        attrs = {"class": "table table-bordered table-dark"}