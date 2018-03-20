from django.shortcuts import render

# Create your views here.

def inicio(request):
    context = {}
    return render(request, 'pages/inicio.html', context)