import django_tables2 as tables
from src.user.models import BaseUser
from src.cms.models.cinema import Hall



class HallTable(tables.Table):
    number = tables.Column(verbose_name='Название')
    date_create = tables.DateTimeColumn(
        verbose_name='Дата создания',
        format='d.m.Y'
    )

    class Meta:
        orderable = False

        model = Hall
        template_name = "django_tables2/bootstrap4.html"
        fields = ('number', 'date_create')
        attrs = {"class": "table table-bordered table-primary"}




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