from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
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
    #return render(request, 'pages/inicio.html', context)
    return  redirect('buscar')

def buscar(request):

    q = request.GET.get('q','')
    e = request.GET.get('e','')
    d = request.GET.get('d','')
    tipos = request.GET.get('t','u,h,a,l').split(',')

    if len(tipos) == 0:
        tipos = 't', 'u,h,a,l'.split(',')

    page_size = request.GET.get('s',6)
    page_num = request.GET.get('p',1)


    if is_number(page_size):
        page_size = int(page_size)
    else:
        page_size = 10

    if is_number(page_num):
        page_num = int(page_num)
    else:
        page_num = 1

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

    def getInt(val):
        if is_number(val):
            return int(val)
        else:
            return -1

    # -----------------------------------------------------
    # Filtros disciplinas
    # -----------------------------------------------------

    filtros_disciplinas = [getInt(x['disciplinas']) for x in qs_ejemplos.values('disciplinas').distinct()]
    filtros_disciplinas += [getInt(x['ejemplos_de_uso__disciplinas']) for x in qs_herramientas.values('ejemplos_de_uso__disciplinas').distinct()]
    filtros_disciplinas += [getInt(x['ejemplo_de_uso__disciplinas']) for x in qs_archivos.values('ejemplo_de_uso__disciplinas').distinct()]
    filtros_disciplinas += [getInt(x['herramienta__ejemplos_de_uso__disciplinas']) for x in qs_tutoriales.values('herramienta__ejemplos_de_uso__disciplinas').distinct()]

    # /----------------------------------------------------

    # -----------------------------------------------------
    # Filtros estrategías
    # -----------------------------------------------------

    filtros_estrategias = [getInt(x['estrategia']) for x in qs_ejemplos.values('estrategia').distinct()]
    filtros_estrategias += [getInt(x['ejemplos_de_uso__estrategia']) for x in qs_herramientas.values('ejemplos_de_uso__estrategia').distinct()]
    filtros_estrategias += [getInt(x['ejemplo_de_uso__estrategia']) for x in qs_archivos.values('ejemplo_de_uso__estrategia').distinct()]
    filtros_estrategias += [getInt(x['herramienta__ejemplos_de_uso__estrategia']) for x in qs_tutoriales.values('herramienta__ejemplos_de_uso__estrategia').distinct()]


    # /----------------------------------------------------

    # -----------------------------------------------------
    # Filtros resultados
    # -----------------------------------------------------

    filtros_resultados = []
    if qs_ejemplos.count()>0:
        filtros_resultados+=(IdNombre('u','Ejemplos de uso'),)
    if qs_herramientas.count()>0:
        filtros_resultados+=(IdNombre('h','Herramientas'),)
    if qs_archivos.count()>0:
        filtros_resultados+=(IdNombre('a','Archivos'),)
    if qs_tutoriales.count()>0:
        filtros_resultados+=(IdNombre('l','Tutoriales'),)

    # /----------------------------------------------------


    if len(d) > 0:

        d = [getInt(x) for x in d.split(",")]
        filtros_disciplinas = chain(filtros_disciplinas,d);

        qs_ejemplos = qs_ejemplos.filter(disciplinas__in=d)
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__disciplinas__in=d)
        qs_archivos = qs_archivos.filter(ejemplo_de_uso__disciplinas__in=d)
        qs_tutoriales = qs_tutoriales.filter(herramienta__ejemplos_de_uso__disciplinas__in=d)


    if len(e) > 0:

        e = [getInt(x) for x in e.split(",")]
        filtros_estrategias = chain(filtros_estrategias,e);

        qs_ejemplos= qs_ejemplos.filter(estrategia_id__in=e)
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__estrategia_id__in=e)
        qs_archivos = qs_archivos.filter(ejemplo_de_uso__estrategia_id__in=e)
        qs_tutoriales = qs_tutoriales.filter(herramienta__ejemplos_de_uso__estrategia_id__in=e)


    if 'u' in tipos:
        qs_ejemplos = qs_ejemplos.distinct().order_by('nombre')
    else: qs_ejemplos = []

    if 'h' in tipos:
        qs_herramientas = qs_herramientas.distinct().order_by('nombre')
    else: qs_herramientas = []

    if 'a' in tipos:
        qs_archivos = qs_archivos.distinct().order_by('nombre')
    else: qs_archivos=[]

    if 'l' in tipos:
        qs_tutoriales = qs_tutoriales.distinct().order_by('nombre')
    else: qs_tutoriales=[]

    chained_list = list(chain(qs_ejemplos, qs_herramientas, qs_archivos,qs_tutoriales))

    # ascending order
    result_list = sorted(chained_list,key=lambda obj: obj.nombre.upper())

    # https://docs.djangoproject.com/en/2.0/topics/pagination/
    paginator = Paginator(result_list,page_size)

    if page_num > paginator.num_pages:
        page_num = paginator.num_pages

    # Calcular paginas que serán visibles en el paginador
    start = page_num - 3
    if start<= 0:
        start = 1

    end = start+7
    if end > paginator.num_pages:
        end = paginator.num_pages+1

    if end-start <7:
        start= end -7
        if start <= 0:
            start = 1

    page = paginator.page(page_num)

    context = {'range':range(start, end),"resultados":page,"disciplinas":Disciplina.objects.all(),"estrategias":Estrategia_Pedagogica.objects.all(),"filtros_resultados":filtros_resultados}

    filtros_disciplinas = list(set(filtros_disciplinas))
    filtros_estrategias = list(set(filtros_estrategias))

    filtros_disciplinas = Disciplina.objects.filter(id__in = filtros_disciplinas)
    filtros_estrategias = Estrategia_Pedagogica.objects.filter(id__in=filtros_estrategias)

    context['filtros_disciplinas'] = filtros_disciplinas
    context['filtros_estrategias'] = filtros_estrategias

    return render(request,'pages/resultados.html', context)

def info_herramienta(request,slug):
    herramienta = get_object_or_404(Herramienta,slug=slug)
    context = {"herramienta":herramienta}
    return render(request,'pages/info_herramienta.html', context)

def info_ejemplo_de_uso(request,slug):
    ejemplo_de_uso = get_object_or_404(Ejemplo_De_Uso,slug=slug)
    context = {"ejemplo_de_uso":ejemplo_de_uso}
    return render(request,'pages/info_ejemplo_de_uso.html', context)

def info_persona_de_conectate(request,slug):
    persona_de_conectate = get_object_or_404(Persona_De_Conectate,slug=slug)
    context = {"persona_de_conectate":persona_de_conectate}
    return render(request,'pages/info_persona_de_conectate.html', context)

def personal(request):
    personas_de_conectate = get_list_or_404(Persona_De_Conectate)
    herramientas = get_list_or_404(Herramienta)
    context = {"personas_de_conectate":personas_de_conectate, "herramientas": herramientas}
    return render(request,'pages/personal.html', context)

def tutoriales(request,slug_herramienta,slug_tutorial):
    tutorial = Tutorial.objects.filter(slug=slug_tutorial,herramienta__slug=slug_herramienta)
    if tutorial.count()==0:
        return HttpResponseNotFound()
    tutoriales = Tutorial.objects.filter(herramienta__slug=slug_herramienta)
    context = {"tutorial":tutorial.first(),"tutoriales":tutoriales,"slug_tutorial":slug_tutorial}
    return render(request,'pages/tutoriales.html', context)

@require_http_methods(["POST"])
def rest_login(request):
    usuario = request.POST.get('usuario','')
    password = request.POST.get('password','')
    user = authenticate(request, username=usuario, password=password)
    status = 400
    message = ""
    if user is not None:
        login(request, user)
        status = 200
        message = user.email

    else:
        message = "Credenciales invalidas."
    return JsonResponse({'status': status, 'message': message})


def logout_view(request):
    logout(request)
    return redirect('inicio')

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

