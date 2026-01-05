
from django.forms import modelformset_factory
from django import forms


from .models import Movie, SeoBlock, Updates, Gallery

from src.cms.models.cinema import Cinema, Hall
from src.cms.models.page import Updates

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




class SeoBlockForm(forms.ModelForm):

    class Meta:
        model = SeoBlock
        fields = "__all__"

        widgets = {
            'url':forms.URLInput(attrs={
                'class':'form-control',
                'placeholder':'Url'

            }),
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Title'
            }),
            'key_words':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Words'
            }),

            'description':forms.Textarea(attrs={
                'class':'form-control',
                'aria-label': 'With textarea',
                'rows': 2,
                'placeholder': 'Description'

            })
        }


        labels = {
            'url':'URL:',
            'title':'Title:',
            'key_words':'Word:',
            'description':'Description:'
        }



class CinemaForm(forms.ModelForm):


    class Meta:
        model = Cinema
        fields = ("title_ru", "title_en","description_ru","description_en" , "conditions", "main_image", "image_top_banner")

# "title, description, conditions, main_image, image_top_banner"
        widgets = {
            'title_ru':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'название кинотеатра'
            }),
            'title_en':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cinema title'
            }),




            'description_ru':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label':'With textarea',
                'placeholder': 'Текст',
                'rows': 4,
            }),


            'description_en':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label':'With textarea',
                'placeholder': 'Text',
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


            }),


        }



class GalleryFrom(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'd-none'}),
        }

class HallForm(forms.ModelForm):

    class Meta:
        model = Hall
        fields =   ['number', 'description', 'scheme_image', 'top_banner_image']

        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер зала'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label': 'With textarea',
                'placeholder': 'Текст',
                'rows': 4,
            }),


            'scheme_image': forms.FileInput(attrs={
                'class': 'd-none',

            }),
            'top_banner_image': forms.FileInput(attrs={
                'class': 'd-none',

            }),

        }


class UpdatesForm(forms.ModelForm):
    class Meta:
        model = Updates

        exclude = ('content_type',)

        widgets = {
            'title_ru':forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'title_en':forms.TextInput(attrs={
                'class': 'form-control',

            }),




            'description_ru':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label':'With textarea',

                'rows': 4,
            }),


            'description_en':forms.Textarea(attrs={
                'class': 'form-control',
                'aria-label':'With textarea',

                'rows': 4,
            }),

            'main_image': forms.FileInput(attrs={
                'class': 'd-none',

            }),

            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ссылка на видео Youtube',
            }),
            'publication_data': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',

            }),

            'is_active': forms.CheckboxInput(attrs={
                'id': 'newsStatusToggle'
            }),
        }

    def clean_main_image(self):
        image = self.cleaned_data.get('main_image')
        if not image and self.instance.pk:
            # если редактируем и файла нет, оставляем старый
            return self.instance.main_image
        return image


GalleryFormSet = modelformset_factory(
    Gallery,
    form= GalleryFrom,
    can_delete=True,
    extra=1
)








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






