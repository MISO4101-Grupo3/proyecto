from django.contrib.auth.models import User
from django.http import SimpleCookie
from django.test import TestCase, Client
from rest_framework.utils import json


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'prueba',
            'password': 'holamundo'}
        User.objects.create_user(**self.credentials)
        self.credentials = {
            'usuario': 'prueba',
            'password': 'holamundo'}

    # Caso de prueba 1:
    # Las credenciales son incorrectas
    def test_login01(self):
        self.credentials['password'] = '#EstaNoEs'

        # Iniciar sesión.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(200,response.status_code,"El codigo de respuesta es incorrecto.")
        self.assertEqual(400,response_content['status'],"El status es incorrecto.")
        self.assertTrue('message' in response_content, "No se indico mensaje de error.")
        self.assertFalse('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")

        # El usuario no debería estar autenticado
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

    # Caso de prueba 2:
    # Las credenciales son válidas
    def test_login02(self):
        # Sin haber iniciado sesión el usuario no debería estar autenticado.
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

        # Iniciar sesión.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(200,response.status_code,"El codigo de respuesta es incorrecto.")
        self.assertEqual(200,response_content['status'],"El status es incorrecto.")
        self.assertTrue('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")

        # Una vez iniciado sesión el usuario debería estar autenticado.
        response = self.client.get('/buscar')
        self.assertTrue(response.context['user'].is_authenticated)

    # Caso de prueba 4:
    # Se cierra sesión correctamente.
    def test_logout03(self):
        # Iniciar sesión.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        self.assertTrue('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")
        sessionid = response.cookies['sessionid']

        # Cerrar sesión
        response = self.client.get('/auth/logout', follow=True)
        self.assertEqual("",response.cookies['sessionid'].value, "No se eliminó la cookie de sesión.")

        # No debería estar autenticado
        self.client.cookies = SimpleCookie({'sessionid': sessionid})
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)
