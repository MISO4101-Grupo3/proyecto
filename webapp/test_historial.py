from unittest import TestCase
from webapp.models import Historial
from django.contrib.auth.models import User


class TestHistorial(TestCase):

    def test_save_amount_registries(self):
        user = User.objects.create_user(username="caev03", password="12345")
        userr = User.objects.create_user(username="caev04", password="23456")
        Historial(busqueda="moodle&d=1&e=1", user=user).save()
        Historial(busqueda="moodle&d=2&e=2", user=userr).save()
        Historial(busqueda="moodle&d=3&e=3", user=user).save()
        historias = Historial.objects.all().filter(user=user)
        self.assertEqual(historias.__len__(),2,"Solo un elemento en el historial")

    def test_save_correct_user(self):
        user = User.objects.create_user(username="caev05", password="12345")
        userr = User.objects.create_user(username="caev06", password="23456")
        Historial(busqueda="moodle&d=1&e=1", user=user).save()
        Historial(busqueda="moodle&d=2&e=2", user=userr).save()
        Historial(busqueda="moodle&d=3&e=3", user=user).save()
        historias = Historial.objects.all().filter(user=user)
        for historia in historias:
            self.assertEqual(historia.user,user,"el Usuario es el correcto")