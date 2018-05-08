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

        # Iniciar sesión via ajax.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(200, response.status_code, "El codigo de respuesta es incorrecto.")
        self.assertEqual(400, response_content['status'], "El status es incorrecto.")
        self.assertTrue('message' in response_content, "No se indico mensaje de error.")
        self.assertFalse('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")

        # El usuario no debería estar autenticado
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

        # Iniciar sesión en la página de ingresar
        data = {
            'usuario': self.credentials['usuario'],
            'contrasenia': self.credentials['password'],
            'accion': 'login'
        }

        # Contraseña incorrecta
        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

        self.assertTrue('contrasenia' in response.context['login_form'].errors)
        self.assertIsNotNone(response.context['login_form'].errors['contrasenia'])
        self.assertFalse('usuario' in response.context['login_form'].errors)
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

        # Usuario incorrecto
        data['usuario'] = 'noexisto@conectate.co'
        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

        self.assertTrue('usuario' in response.context['login_form'].errors)
        self.assertIsNotNone(response.context['login_form'].errors['usuario'])
        self.assertFalse('contrasenia' in response.context['login_form'].errors)
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

    # Caso de prueba 2:
    # Las credenciales son válidas
    def test_login02(self):
        # Sin haber iniciado sesión el usuario no debería estar autenticado.
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

        # Iniciar sesión via ajax.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        response_content = json.loads(str(response.content, encoding='utf8'))
        self.assertEqual(200, response.status_code, "El codigo de respuesta es incorrecto.")
        self.assertEqual(200, response_content['status'], "El status es incorrecto.")
        self.assertTrue('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")

        # Una vez iniciado sesión el usuario debería estar autenticado.
        response = self.client.get('/buscar')
        self.assertTrue(response.context['user'].is_authenticated)

        # Cerrar sesión
        self.client.get('/auth/logout', follow=True)

        # Iniciar sesión en la pagina de ingresar
        data = {
            'usuario': self.credentials['usuario'],
            'contrasenia': self.credentials['password'],
            'accion': 'login'
        }

        response = self.client.post('/ingresar', data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue('sessionid' in response.client.cookies, "La respuesta no contiene la cookie de sesión.")

    # Caso de prueba 4:
    # Se cierra sesión correctamente.
    def test_logout03(self):
        # Iniciar sesión via ajax.
        response = self.client.post('/auth/login', self.credentials, follow=True)
        self.assertTrue('sessionid' in response.cookies, "La respuesta no contiene la cookie de sesión.")
        sessionid = response.cookies['sessionid']

        # Cerrar sesión
        response = self.client.get('/auth/logout', follow=True)
        self.assertEqual("", response.cookies['sessionid'].value, "No se eliminó la cookie de sesión.")

        # No debería estar autenticado
        self.client.cookies = SimpleCookie({'sessionid': sessionid})
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

        # Iniciar sesión en la pagina de ingresar

        data = {
            'usuario': self.credentials['usuario'],
            'contrasenia': self.credentials['password'],
            'accion': 'login'
        }

        response = self.client.post('/ingresar', data, follow=True)

        # Cerrar sesión
        response = self.client.get('/auth/logout', follow=True)
        self.assertEqual("", response.cookies['sessionid'].value, "No se eliminó la cookie de sesión.")

        # No debería estar autenticado
        self.client.cookies = SimpleCookie({'sessionid': sessionid})
        response = self.client.get('/buscar')
        self.assertFalse(response.context['user'].is_authenticated)

    # Caso de prueba 5:
    # 1. Prueba el registro con datos inválidos
    # 2. Prueba el registro con datos validos
    # 3. Verifica que no se pueda registrar nuevamente
    # 4. Prueba el login con el usuario registrado
    def test_registro01(self):
        data = {
            'username': 'h.mundo10@test.co',
            'password1': '12345678',
            'password2': '1234567',
            'terminos': False,
            'accion': 'registrar'
        }

        # 1. datos inválidos
        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue('password2' in response.context['registro_form'].errors)
        self.assertTrue('first_name' in response.context['registro_form'].errors)
        self.assertTrue('last_name' in response.context['registro_form'].errors)
        self.assertTrue('terminos' in response.context['registro_form'].errors)
        self.assertTrue('username' in response.context['registro_form'].errors)

        data['username'] = 'h.mundo10'
        data['first_name'] = 'Hola'
        data['last_name'] = 'Mundo'
        data['password2'] = '12345678'
        data['terminos'] = True

        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue('password2' in response.context['registro_form'].errors)

        # 2. Datos válidos
        data['password1'] = '#WTFP4SSW'
        data['password2'] = '#WTFP4SSW'

        response = self.client.post('/ingresar', data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue('sessionid' in response.client.cookies, "La respuesta no contiene la cookie de sesión.")
        usuario = User.objects.filter(username=data['username'])
        self.assertEqual(1, usuario.count())
        usuario = usuario.get()
        self.assertEqual(data['first_name'], usuario.first_name)
        self.assertEqual(data['last_name'], usuario.last_name)
        self.assertEqual(data['username'] + '@uniandes.edu.co', usuario.email)

        self.client.get('/auth/logout', follow=True)

        # 3. No se puede volver a registrar
        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue('username' in response.context['registro_form'].errors)

        data['username'] = data['username'] + '@uniandes.edu.co'

        response = self.client.post('/ingresar', data, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertTrue('username' in response.context['registro_form'].errors)

        # 4. Probar login con el usuario registrado
        data = {
            'usuario': data['username'],
            'contrasenia': data['password2'],
            'accion': 'login'
        }

        # Con @uniandes.edu.co
        response = self.client.post('/ingresar', data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue('sessionid' in response.client.cookies, "La respuesta no contiene la cookie de sesión.")

        self.client.get('/auth/logout', follow=True)

        # Sin @uniandes.edu.co
        data['usuario'] = data['usuario'].replace('@uniandes.edu.co', '')
        response = self.client.post('/ingresar', data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated, "El usuario debió quedar autenticado.")
        self.assertTrue('sessionid' in response.client.cookies, "La respuesta no contiene la cookie de sesión.")
