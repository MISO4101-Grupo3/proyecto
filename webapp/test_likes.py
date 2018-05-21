from unittest import TestCase
from webapp.models import Herramienta, Ejemplo_De_Uso, Tutorial, Estrategia_Pedagogica


class TestLikes(TestCase):

    def test_like_tool(self):
        tool = Herramienta(descripcion="test",tipo_de_licencia="MIT", sitio="test.html",descarga="test.html", restricciones_de_uso="No", nombre="test", descripcion_funcional="test", sistemas_operativos="Windows", version="1.0.1",integracion_con_lms=True,slug="asdasd")
        self.assertEqual(tool.likes, 0)
        tool.likeObject()
        self.assertEqual(tool.likes, 1)
        tool.likeObject()
        tool.likeObject()
        tool.likeObject()
        tool.likeObject()
        tool.likeObject()
        self.assertEqual(tool.likes, 6)

    def test_like_example(self):
        strategia = Estrategia_Pedagogica(nombre="teest")
        strategia.save()
        strategia = Estrategia_Pedagogica.objects.all().filter(nombre="teest").first()
        example = Ejemplo_De_Uso(descripcion="test",nombre="test",slug="test", estrategia=strategia)
        self.assertEqual(example.likes, 0)
        example.likeObject()
        self.assertEqual(example.likes, 1)
        example.likeObject()
        example.likeObject()
        example.likeObject()
        example.likeObject()
        example.likeObject()
        self.assertEqual(example.likes, 6)

    def test_like_tutorial(self):
        toool = Herramienta(descripcion="teest",tipo_de_licencia="MIIT", sitio="teest.html",descarga="teest.html", restricciones_de_uso="Noo", nombre="teest", descripcion_funcional="teest", sistemas_operativos="Window", version="1.0.2",integracion_con_lms=True,slug="teesst")
        toool.save()
        toool = Herramienta.objects.all().filter(slug="teesst").first()
        tutorial = Tutorial(nombre="test", descripcion="test", url_recurso="sadasd.html", slug="ttest", herramienta=toool)
        self.assertEqual(tutorial.likes, 0)
        tutorial.likeObject()
        self.assertEqual(tutorial.likes, 1)
        tutorial.likeObject()
        tutorial.likeObject()
        tutorial.likeObject()
        tutorial.likeObject()
        tutorial.likeObject()
        self.assertEqual(tutorial.likes, 6)



        