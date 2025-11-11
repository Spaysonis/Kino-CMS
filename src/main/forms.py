from django import forms
from django.contrib.auth.forms import UserCreationForm
from src.user.models import BaseUser



class SimpleRegistrationForm(UserCreationForm):
    """ПРОСТАЯ ФОРМА ДЛЯ РЕГИСТРАЦИИ НА САЙТЕ"""
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = BaseUser
        fields = ('username', 'email', 'password1', 'password2')



class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""
    class Meta:
        model = BaseUser
        fields = ['first_name', 'last_name', 'nick_name', 'phone_num', 'city', 'address', 'gender', 'date_of_birth', 'language']

        widgets = {


            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'nick_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите псевдоним'
            }),
            'phone_num': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите телефон'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите город'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'language': forms.Select(attrs={
                'class': 'form-control'
            }),
        }