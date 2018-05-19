from django.urls import path
from django.conf.urls import url
from webapp import views

urlpatterns = [
    path('', views.inicio , name='inicio'),
    path('buscar', views.buscar , name='buscar'),
    path('herramientas/<slug:slug>', views.info_herramienta , name='herramientas'),
    path('ejemplos/<slug:slug>', views.info_ejemplo_de_uso , name='ejemplos'),
    path('personal/<slug:slug>', views.info_persona_de_conectate , name='personal'),
    path('like/<path:path>/<str:superClass>/<str:detailed>/<slug:slug>', views.like, name='likeObject'),
    path('like/<str:strTutorial>/<str:detailed>/<slug:herramienta>/<slug:tutorial>/<path:path>', views.likeTutorial, name='likeTutorial'),
    path('personal', views.personal , name='personal_dashboard'),
    path('herramientas/<slug:slug_herramienta>/tutoriales/<slug:slug_tutorial>', views.tutoriales , name='tutoriales'),
    path('auth/login', views.rest_login, name='login'),
    path('ingresar', views.login_register, name='ingresar'),
    path('auth/logout', views.logout_view, name='logout'),
    path('historial', views.historial, name="historial"),
    path('comentario', views.rest_add_comment, name='anadir_comentario')
]
