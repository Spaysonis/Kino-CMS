from django import forms
from django.contrib.auth.forms import UserCreationForm
from src.user.models import BaseUser


class SimpleRegistrationForm(UserCreationForm):
    """ПРОСТАЯ ФОРМА ДЛЯ РЕГИСТРАЦИИ НА САЙТЕ"""
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = BaseUser
        fields = ('username', 'email', 'password1', 'password2')



class ProfileEditForm(UserCreationForm):
    """ДОБАВЛЯЮ В БД ОСТАЛЬНЫЕ ПОЛЯ ДЛЯ ПОЛЬЗОВАТЕЛЯ"""
    class Meta:
        model = BaseUser
        fields = ('nick_name', 'phone_num', 'city', 'address', 'gender', 'date_of_birth', 'language')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[
                ('', 'Выберите пол'),
                ('male', 'Мужской'),
                ('female', 'Женский'),
            ]),
            'language': forms.Select(choices=[
                ('ru', 'Русский'),
                ('uk', 'Украинский'),
            ]),
        }
