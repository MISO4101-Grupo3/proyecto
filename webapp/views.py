from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound

from .forms import *
from .models import *
from django.db.models import Q
from functools import reduce
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator

# Create your views here.

def inicio(request):
    context = {}
    return render(request, 'pages/inicio.html', context)

def buscar(request):

    q = request.GET.get('q','')
    e = request.GET.get('e','')
    d = request.GET.get('d','')
    tipos = request.GET.get('t','e,h,a,t').split(',')

    page_size = request.GET.get('s',1)
    page_num = request.GET.get('p',1)


    if is_number(page_size):
        page_size = int(page_size)
    else:
        page_size = 10
    keywords = q.split()


    if len(keywords) > 0:
        # Filtros para ejemplos de uso
        filters = reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(estrategia__nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(disciplinas__nombre__icontains=word) for word in keywords])

        qs_ejemplos = Ejemplo_De_Uso.objects.filter(filters)

        # Filtros para herramientas
        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion_funcional__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(sistemas_operativos__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(restricciones_de_uso__icontains=word) for word in keywords])

        qs_herramientas = Herramienta.objects.filter(filters)

        # Filtros para archivos
        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])

        qs_archivos = Archivo.objects.filter(filters)

        #Filtros para tutoriales
        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(url_recurso__icontains=word) for word in keywords])

        qs_tutoriales = Tutorial.objects.filter(filters)

    else:
        qs_ejemplos = Ejemplo_De_Uso.objects
        qs_herramientas = Herramienta.objects
        qs_archivos = Archivo.objects
        qs_tutoriales = Tutorial.objects

    # Filtro por estrategía

    if len(e) > 0:
        if is_number(e):
            e = int(e)
        else: e = -1

        qs_ejemplos= qs_ejemplos.filter(estrategia_id=e)
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__estrategia_id=e)
        qs_archivos = qs_archivos.filter(ejemplos_de_uso__estrategia_id=e)
        qs_tutoriales = qs_tutoriales.filter(herramienta__ejemplos_de_uso__estrategia_id=e)

    # Filtro por disciplina

    if len(d) > 0:
        if is_number(d):
            d = int(d)
        else: d = -1

        qs_ejemplos = qs_ejemplos.filter(disciplinas__in=[d,])
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__disciplinas__in=[d,])
        qs_archivos = qs_archivos.filter(ejemplos_de_uso__disciplinas__in=[d,])
        qs_tutoriales = qs_tutoriales.filter(herramienta__ejemplos_de_uso__disciplinas__in=[d,])

    # Filtros Resultados
    filtros_resultados = []
    if qs_ejemplos.count()>0:
        filtros_resultados+=(IdNombre('e','Ejemplos de uso'),)
    if qs_herramientas.count()>0:
        filtros_resultados+=(IdNombre('h','Herramientas'),)
    if qs_archivos.count()>0:
        filtros_resultados+=(IdNombre('a','Archivos'),)
    if qs_tutoriales.count()>0:
        filtros_resultados+=(IdNombre('t','Tutoriales'),)

    if 'e' in tipos:
        qs_ejemplos = qs_ejemplos.order_by('nombre')
    else: qs_ejemplos = []

    if 'h' in tipos:
        qs_herramientas = qs_herramientas.order_by('nombre')
    else: qs_herramientas = []

    if 'a' in tipos:
        qs_archivos = qs_archivos.order_by('nombre')
    else: qs_archivos=[]

    if 't' in tipos:
        qs_tutoriales = qs_tutoriales.order_by('nombre')
    else: qs_tutoriales=[]

    chained_list = list(chain(qs_ejemplos, qs_herramientas, qs_archivos,qs_tutoriales))

    # ascending order
    result_list = sorted(chained_list,key=lambda obj: obj.nombre.upper())

    # https://docs.djangoproject.com/en/2.0/topics/pagination/
    paginator = Paginator(result_list,page_size)
    page = paginator.page(page_num)
    return render(request,'pages/resultados.html', {"resultados":page,"disciplinas":Disciplina.objects.all(),"estrategias":Estrategia_Pedagogica.objects.all(),"filtros_resultados":filtros_resultados})

def info_herramienta(request,slug):
    herramienta = get_object_or_404(Herramienta,slug=slug)
    context = {"herramienta":herramienta}
    return render(request,'pages/info_herramienta.html', context)

def info_ejemplo_de_uso(request,slug):
    ejemplo_de_uso = get_object_or_404(Ejemplo_De_Uso,slug=slug)
    context = {"ejemplo_de_uso":ejemplo_de_uso}
    return render(request,'pages/info_ejemplo_de_uso.html', context)


def tutoriales(request,slug_herramienta,slug_tutorial):
    tutorial = Tutorial.objects.filter(slug=slug_tutorial,herramienta__slug=slug_herramienta)
    if tutorial.count()==0:
        return HttpResponseNotFound()
    tutoriales = Tutorial.objects.filter(herramienta__slug=slug_herramienta)
    context = {"tutorial":tutorial.first(),"tutoriales":tutoriales,"slug_tutorial":slug_tutorial}
    return render(request,'pages/tutoriales.html', context)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class IdNombre:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
