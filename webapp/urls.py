from django.urls import path
from django.conf.urls import url
from webapp import views

urlpatterns = [
    path('', views.inicio , name='inicio'),
    path('buscar', views.buscar , name='buscar'),
    path('herramientas/<slug:slug>', views.info_herramienta , name='herramientas'),
    path('ejemplos/<slug:slug>', views.info_ejemplo_de_uso , name='ejemplo_de_uso'),
    path('herramientas/<slug:slug_herramienta>/tutoriales/<slug:slug_tutorial>', views.tutoriales , name='tutoriales'),
]
