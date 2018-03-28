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
    if request.method == 'POST':
        form = BusquedaSimpleForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data.get("query",'')
            keywords = q.split()
            filters = reduce(lambda x, y: x & y, [Q(descripcion__icontains=word) for word in keywords])
            filters |= reduce(lambda x, y: x & y, [Q(nombre__icontains=word) for word in keywords])
            qs = Ejemplo_De_Uso.objects.filter(filters)

    return render(request,'pages/resultados.html')