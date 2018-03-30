from django import forms
from django.conf.locale import sl

from .models import *
from django.http.request import QueryDict
from django.utils.text import slugify

class HerramientaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HerramientaForm, self).__init__(*args, **kwargs)

        # Ensure that data is a regular Python dictionary so we can
        # modify it later.
        if isinstance(self.data, QueryDict):
            self.data = self.data.copy()

        # We assume here that the slug is only generated once, when
        # saving the object. Since they are used in URLs they should
        # not change when valid.
        if not self.instance.pk and self.data.get('nombre'):
            self.data['slug'] = slugify(self.data['nombre'])

    class Meta:
        model = Herramienta
        exclude = ['slug']

    def _post_clean(self):
        super()._post_clean()

        nombre = self.cleaned_data['nombre']
        herramienta = self.instance
        id = herramienta.id
        slug = slugify(nombre)
        qs = Herramienta.objects.filter(slug=slug)
        if qs.count()>0:
            exist = qs.first()
            if exist.id != id :
                self.add_error('nombre',"No se puede crear un slug único con este nombre.")

class TutorialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TutorialForm, self).__init__(*args, **kwargs)

        # Ensure that data is a regular Python dictionary so we can
        # modify it later.
        if isinstance(self.data, QueryDict):
            self.data = self.data.copy()

        # We assume here that the slug is only generated once, when
        # saving the object. Since they are used in URLs they should
        # not change when valid.
        if not self.instance.pk and self.data.get('nombre'):
            self.data['slug'] = slugify(self.data['nombre'])

    class Meta:
        model = Tutorial
        exclude = ['slug']

    def _post_clean(self):
        super()._post_clean()

        nombre = self.cleaned_data['nombre']
        tutorial = self.instance
        id = tutorial.id
        slug = slugify(nombre)
        qs = Tutorial.objects.filter(slug=slug,herramienta_id=tutorial.herramienta_id)
        if qs.count()>0:
            exist = qs.first()
            if exist.id != id :
                self.add_error('nombre',"No se puede crear un slug único con este nombre.")

