from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .utils import *

# Comentario

class Comentario(models.Model):
    def __str__(self):
        return self.descripcion
    
    def class_name(self):
        return self.__class__.__name__

    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(null=True, blank=True, max_length=10)
    id_tipo = models.IntegerField(default=0)
    usuario = models.ForeignKey(User, related_name='usuario_comentario', null=True, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Comentario, self).save(*args, **kwargs)

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


#Areas de experiencia
class Area_De_Experiencia(models.Model):
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural = "areas"
    nombre = models.CharField(null=True, blank=True, max_length=255)

# Archivo

class Archivo(models.Model):
    def __str__(self):
        return  str(self.ejemplo_de_uso)+" : " + str(self.nombre)

    def class_name(self):
        return self.__class__.__name__

    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(null=True, blank=True, max_length=10)
    file = models.FileField(upload_to=UploadToPathAndRename('uploads/archivos'))
    nombre = models.CharField(null=True, blank=True, max_length=200)
    ejemplo_de_uso = models.ForeignKey('Ejemplo_De_Uso', related_name='archivos', null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Archivo, self).save(*args, **kwargs)

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
    nombre = models.CharField(null=True, blank=True, max_length=200)
    descripcion_funcional = models.TextField(null=True, blank=True)
    sistemas_operativos = models.CharField(null=True, blank=True, max_length=255)
    version = models.CharField(null=True, blank=True, max_length=10)
    integracion_con_lms = models.BooleanField(default=False, null=False)
    imagen = models.ImageField(upload_to=UploadToPathAndRename('uploads/imagenes'), null=True)
    slug = models.SlugField(max_length=250, unique=True, null=False, blank=False)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Herramienta, self).save(*args, **kwargs)

    def likeObject(self):
        self.likes = self.likes + 1
        self.save()


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
    slug = models.SlugField(max_length=250, default="")
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Ejemplo_De_Uso, self).save(*args, **kwargs)

    def likeObject(self):
        self.likes = self.likes + 1
        self.save()

# Personal_de_conectate

class Persona_De_Conectate(models.Model):
    def __str__(self):
        return self.nombre

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name_plural = "Personal de conectate"
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="personal", null=True, blank=True)
    nombre = models.CharField(null=True, blank=True, max_length=255)
    perfil = models.TextField(null=True, blank=True)
    herramientas = models.ManyToManyField('Herramienta', related_name='personal_de_conectate', blank=True)
    areas_de_experiencia = models.ManyToManyField('Area_De_Experiencia', related_name='personal_de_conectate', blank=True)
    contacto = models.CharField(null=True, blank=True, max_length=255)
    ejemplos_de_uso = models.ManyToManyField('Ejemplo_De_Uso', related_name='ejemplos_de_uso', blank=True)
    imagen = models.ImageField(upload_to=UploadToPathAndRename('uploads/imagenes'), null=True)
    slug = models.SlugField(max_length=250, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Persona_De_Conectate, self).save(*args, **kwargs)

# Tutorial

class Tutorial(models.Model):
    def __str__(self):
        return self.nombre

    def class_name(self):
        return self.__class__.__name__

    class Meta:
        verbose_name_plural = "Tutoriales"
    nombre = models.CharField(null=True, blank=True, max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    url_recurso = models.URLField(null=True, blank=True)
    herramienta = models.ForeignKey('Herramienta', related_name='tutoriales', null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=False, blank=False)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Tutorial, self).save(*args, **kwargs)

    def likeObject(self):
        self.likes = self.likes + 1
        self.save()

class Historial(models.Model):

    def __str__(self):
        return self.busqueda
    
    def class_name(self):
        return self.__class__.__name__

    fecha = models.DateTimeField(auto_now_add=True)
    busqueda = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='usuario', null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Historial, self).save(*args, **kwargs)
