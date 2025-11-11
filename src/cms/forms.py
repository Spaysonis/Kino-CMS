from django import forms
from .models.cinema import Movie
from .models.page import SeoBlock

from django import forms
from .models import Movie, SeoBlock


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