

from django import forms
from .models import Movie, SeoBlock, Updates

from src.cms.models.cinema import Cinema

from ..user.models import BaseUser


class UserEditForm(forms.ModelForm):

    class Meta:
        model = BaseUser
        fields = ['first_name', 'last_name', 'nick_name', 'phone_num', 'city', 'address', 'gender', 'date_of_birth',
                  'language', 'email', 'password', 'card_num' ]

        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'nick_name' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'}),
            'card_num' : forms.TextInput(attrs={'class':'form-control'}),
            'address' : forms.TextInput(attrs={'class':'form-control'}),
            'language' : forms.RadioSelect(attrs={'class':'form-check-input'}),
            'gender' : forms.RadioSelect(attrs={'class':'form-check-input'}),
            'phone_num' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.Select(attrs={'class':'custom-select'}),
            'date_of_birth' : forms.DateInput(attrs={'class':'form-control',
                                                     'type':'date'}),

        }


class CinemaForm(forms.ModelForm):


    class Meta:
        model = Cinema
        fields = ("title", "description", "conditions", "main_image", "image_top_banner")

# "title, description, conditions, main_image, image_top_banner"
        widgets = {
            'title':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'название кинотеатра'
            }),
            'description':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label':'With textarea',
                'placeholder': 'Текст',
                'rows': 4,
            }),

            'conditions':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label': 'With textarea',
                'placeholder': 'Текст',
                'rows': 4,

            }),
            'main_image':forms.FileInput(attrs={
                'class':'d-none',


            }),
            'image_top_banner':forms.FileInput(attrs={
                'class':'d-none',


            })
        }



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['gallery', 'title', 'description', 'main_image', 'url',
                  'format_2d', 'format_3d', 'format_imax']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'Введите название фильма'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'Введите описание фильма',
                'rows': 6
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'https://example.com'
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'gallery': forms.SelectMultiple(attrs={
                'class': 'form-select border-0 bg-dark text-light'
            }),
            'format_2d': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'format_3d': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'format_imax': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['url', 'title', 'key_words', 'description']

        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'SEO URL'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'SEO Title'
            }),
            'key_words': forms.TextInput(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'Ключевые слова через запятую'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control border-0 bg-dark text-light',
                'placeholder': 'Мета-описание',
                'rows': 3
            }),
        }




class NewsForm(forms.ModelForm):

    class Meta:
        model = Updates
        fields = "__all__"

        widgets = {
            'is_active': forms.CheckboxInput(attrs=
                                             {'class':'custom-control-input',
                                              'id':'news_switch'}),
            # 'title': forms.TextInput(attrs=
            #                          {'class':'form-control',
            #                           'style':'width: 200px'
            # }),
            #
            # 'publication_data':forms.DateInput(attrs={
            #                                    'type':'date',
            #                                     'class':'form-control',
            #                                     'style': 'width: 200px'
            #                                    }),
            #
            # 'description':forms.Textarea(attrs={'class': 'form-control',
            #                                     'rows': 3,
            #                                     'id': 'text_description',
            #
            #
            #
            # })
        }

        labels = {
            'is_active': 'ВКЛ',
            'title': 'Название новости',
            'publication_data':'Дата публикации',
            'description': 'Описание новости',

        }