from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class HerramientaAdmin(admin.ModelAdmin):
    form = HerramientaForm

admin.site.register(Disciplina)
admin.site.register(Estrategia_Pedagogica)
admin.site.register(Archivo)
admin.site.register(Herramienta, HerramientaAdmin)
admin.site.register(Ejemplo_De_Uso)
admin.site.register(Tutorial)