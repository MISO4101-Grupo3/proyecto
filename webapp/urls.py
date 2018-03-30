from django.urls import path
from django.conf.urls import url
from webapp import views

urlpatterns = [
    path('', views.inicio , name='inicio'),
    path('buscar', views.buscar , name='buscar'),
    path('herramientas/<slug:slug>', views.info_herramienta , name='herramientas'),

]
