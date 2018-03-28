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
    keywords = q.split()
    print(q)
    print(keywords)
    if len(keywords) > 0:
        # Filtros para ejemplos de uso
        filters = reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(estrategia__nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(disciplinas__nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(herramientas__nombre__icontains=word) for word in keywords])

        qs_ejemplos = Ejemplo_De_Uso.objects.filter(filters).all()

        # Filtros para herramientas
        filters = reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(descripcion_funcional__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(sistemas_operativos__icontains=word) for word in keywords])
        filters |= reduce(lambda x, y: x & y, [Q(restricciones_de_uso__icontains=word) for word in keywords])

        qs_herramientas = Herramienta.objects.filter(filters).all()

    else:
        qs_ejemplos = Ejemplo_De_Uso.objects.all()
        qs_herramientas = Herramienta.objects.all()


    print(qs_ejemplos)
    print(qs_herramientas)
    return render(request,'pages/resultados.html', {"herramientas":qs_herramientas,"ejemplos":qs_ejemplos})