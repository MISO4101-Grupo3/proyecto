from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class HerramientaAdmin(admin.ModelAdmin):
    form = HerramientaForm

class Ejemplo_De_UsoAdmin(admin.ModelAdmin):
    form = Ejemplo_De_UsoForm

class TutorialAdmin(admin.ModelAdmin):
    form = TutorialForm

admin.site.register(Disciplina)
admin.site.register(Estrategia_Pedagogica)
admin.site.register(Archivo)
admin.site.register(Herramienta, HerramientaAdmin)
admin.site.register(Ejemplo_De_Uso, Ejemplo_De_UsoAdmin )
admin.site.register(Tutorial, TutorialAdmin)
