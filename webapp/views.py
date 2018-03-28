from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from django.db.models import Q
from functools import reduce

# Create your views here.

def inicio(request):
    context = {}
    return render(request, 'pages/inicio.html', context)

def buscar(request):

    q = request.GET.get('q','')
    e = request.GET.get('e','')
    d = request.GET.get('d','')

    keywords = q.split()

    if len(keywords) > 0:
        # Filtros para ejemplos de uso
        filters = reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(estrategia__nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(disciplinas__nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(herramientas__nombre__icontains=word) for word in keywords])

        qs_ejemplos = Ejemplo_De_Uso.objects.filter(filters)

        # Filtros para herramientas
        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion_funcional__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(sistemas_operativos__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(restricciones_de_uso__icontains=word) for word in keywords])

        qs_herramientas = Herramienta.objects.filter(filters)

        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(tipo__icontains=word) for word in keywords])

        qs_archivos = Archivo.objects.filter(filters)

    else:
        qs_ejemplos = Ejemplo_De_Uso.objects
        qs_herramientas = Herramienta.objects
        qs_archivos = Archivo.objects

    # Filtro por estrategía

    if len(e) > 0:
        if is_number(e):
            e = int(e)
        else: e = -1

        qs_ejemplos= qs_ejemplos.filter(estrategia_id=e)
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__estrategia_id=e)
        qs_archivos = qs_archivos.filter(ejemplos_de_uso__estrategia_id=e)

    # Filtro por disciplina

    if len(d) > 0:
        if is_number(d):
            d = int(d)
        else: d = -1

        qs_ejemplos = qs_ejemplos.filter(disciplinas__in=[d,])
        qs_herramientas = qs_herramientas.filter(ejemplos_de_uso__disciplinas__in=[d,])
        qs_archivos = qs_archivos.filter(ejemplos_de_uso__disciplinas__in=[d,])

    qs_ejemplos = qs_ejemplos.all()
    qs_herramientas = qs_herramientas.all()
    qs_archivos = qs_archivos.all()

    return render(request,'pages/resultados.html', {"herramientas":qs_herramientas,"ejemplos":qs_ejemplos,"archivos":qs_archivos,"disciplinas":Disciplina.objects.all(),"estrategias":Estrategia_Pedagogica.objects.all()})


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