from django.db import models
from django.contrib.auth.models import User
from .utils import *

# Disciplina

class Disciplina(models.Model):
    def __str__(self):
        return  self.nombre
    nombre = models.CharField(null=True, blank=True, max_length=50)


# Estrategia_Pedagogica

class Estrategia_Pedagogica(models.Model):
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "estrategías"
    nombre = models.CharField(null=True, blank=True, max_length=255)

# Archivo

class Archivo(models.Model):
    def __str__(self):
        return 'id:'+ str(self.id)

    def class_name(self):
        return self.__class__.__name__

    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(null=True, blank=True, max_length=10)
    file = models.FileField(upload_to=UploadToPathAndRename('uploads/archivos'))
    nombre = models.CharField(null=True, blank=True, max_length=255)
    ejemplo_de_uso = models.ForeignKey('Ejemplo_De_Uso', related_name='archivos', null=True, on_delete=models.CASCADE)

# Herramienta

class Herramienta(models.Model):
    def __str__(self):
        return self.nombre


    def class_name(self):
        return self.__class__.__name__

    descripcion = models.TextField(null=True, blank=True)
    tipo_de_licencia = models.CharField(null=True, blank=True, max_length=50)
    sitio = models.URLField(null=True, blank=True)
    descarga = models.URLField(null=True, blank=True)
    restricciones_de_uso = models.TextField(null=True, blank=True)
    nombre = models.CharField(null=True, blank=True, max_length=255)
    descripcion_funcional = models.TextField(null=True, blank=True)
    sistemas_operativos = models.CharField(null=True, blank=True, max_length=255)
    version = models.CharField(null=True, blank=True, max_length=10)
    integracion_con_lms = models.BooleanField(default=False, null=False)
    imagen = models.ImageField(upload_to=UploadToPathAndRename('uploads/imagenes'), null=True)



# Ejemplo_De_Uso

class Ejemplo_De_Uso(models.Model):
    def __str__(self):
        return self.nombre

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name_plural = "Ejemplos de uso"
    nombre = models.CharField(null=True, blank=True, max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    disciplinas = models.ManyToManyField('Disciplina', related_name='ejemplos_de_uso', blank=True)
    herramientas = models.ManyToManyField('Herramienta', related_name='ejemplos_de_uso', blank=True)
    estrategia = models.ForeignKey('Estrategia_Pedagogica', related_name='ejemplos_de_uso', on_delete=models.CASCADE)

# Tutorial

class Tutorial(models.Model):
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "Tutoriales"
    nombre = models.CharField(null=True, blank=True, max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    url_recurso = models.URLField(null=True, blank=True)
    herramienta = models.ForeignKey('Herramienta', related_name='tutoriales', null=True, on_delete=models.CASCADE)