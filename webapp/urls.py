from django.urls import path
from django.conf.urls import url
from webapp import views

urlpatterns = [
    path('', views.inicio , name='inicio'),
    path('buscar', views.buscar , name='buscar'),
    path('herramientas/<slug:slug>', views.info_herramienta , name='herramientas'),
    path('ejemplos/<slug:slug>', views.info_ejemplo_de_uso , name='ejemplos'),
    path('personal/<slug:slug>', views.info_persona_de_conectate , name='personal'),
    path('editar/', views.edit_persona_de_conectate , name='editar'),
    path('personal', views.personal , name='personal_dashboard'),
    path('herramientas/<slug:slug_herramienta>/tutoriales/<slug:slug_tutorial>', views.tutoriales , name='tutoriales'),
    path('auth/login', views.rest_login, name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('api/herramientas', views.list_herramientas, name='getherramientas')
    path('ingresar', views.login_register, name='ingresar'),
    path('auth/logout', views.logout_view, name='logout'),
    path('historial', views.historial, name="historial"),
]
