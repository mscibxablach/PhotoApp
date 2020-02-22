from django import forms

from .models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'surname', 'description', 'pdf', 'original')


class WithoutDBPhotoForm(forms.Form):
    name = forms.CharField(label='Imię', max_length=100)
    surname = forms.CharField(label='Nazwisko', max_length=100)
    description = forms.CharField(label='Opis', max_length=100)
    photo = forms.ImageField(label='Zdjęcie')