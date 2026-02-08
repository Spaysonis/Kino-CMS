from django import forms
from django.contrib.auth.forms import UserCreationForm
from src.user.models import BaseUser



class SimpleRegistrationForm(UserCreationForm):


    class Meta:
        model = BaseUser
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control bg-transparent',
                'placeholder':'Логин'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder': 'Email'
            }),
            'password1':forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
        })}



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
            }),'card_num': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер карты'
            }),
        }