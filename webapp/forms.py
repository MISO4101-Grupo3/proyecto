from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from .models import *
from django.http.request import QueryDict
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


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

class Ejemplo_De_UsoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Ejemplo_De_UsoForm, self).__init__(*args, **kwargs)

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
        model = Ejemplo_De_Uso
        exclude = ['slug']

    def _post_clean(self):
        super()._post_clean()

        nombre = self.cleaned_data['nombre']
        ejemplos_de_uso = self.instance
        id = ejemplos_de_uso.id
        slug = slugify(nombre)
        qs = Ejemplo_De_Uso.objects.filter(slug=slug)
        if qs.count()>0:
            exist = qs.first()
            if exist.id != id :
                self.add_error('nombre',"No se puede crear un slug único con este nombre.")



class Persona_De_ConectateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Persona_De_ConectateForm, self).__init__(*args, **kwargs)

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
        model = Persona_De_Conectate
        exclude = ['slug']

    def _post_clean(self):
        super()._post_clean()

        nombre = self.cleaned_data['nombre']
        persona_de_conectate = self.instance
        id = persona_de_conectate.id
        slug = slugify(nombre)
        qs = Persona_De_Conectate.objects.filter(slug=slug)
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

class ArchivoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArchivoForm, self).__init__(*args, **kwargs)

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
        model = Archivo
        exclude = ['slug']

    def _post_clean(self):
        super()._post_clean()

        nombre = self.cleaned_data['nombre']
        archivo = self.instance
        id = archivo.id
        slug = slugify(nombre)
        qs = Archivo.objects.filter(slug=slug,ejemplo_de_uso_id=archivo.ejemplo_de_uso_id)
        if qs.count()>0:
            exist = qs.first()
            if exist.id != id :
                self.add_error('nombre',"No se puede crear un slug único con este nombre.")

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    terminos = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('username','password1','password2','first_name','last_name','terminos')
        error_messages = {
            'first_name': {
                'required': _("Por favor ingresa tus nombres."),
            },
        }

    def clean_terminos(self):
        acepta = self.cleaned_data.get("terminos")
        if not acepta:
            raise forms.ValidationError("Debes aceptar los terminos y condiciones")
        return acepta

    def clean_username(self):
        username = self.cleaned_data.get("username").strip()
        if '@' in username and not username.endswith('@uniandes.edu.co'):
            raise forms.ValidationError("El usuario no pertenece a @uniandes.edu.co")

        q = User.objects.filter(Q(email=username)| Q(username=username))
        if q.count() > 0:
            raise  forms.ValidationError("El usuario ya está registrado.")

        return username.replace('@uniandes.edu.co','')

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=150,required=True)
    contrasenia = forms.CharField(widget=forms.PasswordInput)

    def clean_usuario(self):
        usuario = self.cleaned_data.get("usuario").strip()
        if '@' in usuario and not usuario.endswith('@uniandes.edu.co'):
            raise forms.ValidationError("El usuario no pertenece a @uniandes.edu.co")

        q = User.objects.filter(Q(email=usuario) | Q(username=usuario))
        if q.count() == 0:
            raise forms.ValidationError("El usuario no está registrado.")

        return usuario.replace('@uniandes.edu.co', '')

    def _post_clean(self):
        super()._post_clean()
        usuario = self.cleaned_data.get('usuario')
        user = authenticate(username=usuario, password=self.cleaned_data.get('contrasenia'))
        if User.objects.filter(username=usuario).count()>0 and not user:
            self.add_error('contrasenia', forms.ValidationError("Contraseña incorrecta"))

