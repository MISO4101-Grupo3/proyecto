from django import forms
from .models import *

class BusquedaSimpleForm(forms.Form):
    query = forms.CharField(max_length=50)