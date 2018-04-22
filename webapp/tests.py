from django.test import TestCase
from webapp.models import Persona_De_Conectate

class Persona_De_ConectaTestCase(TestCase):
    """
    PersonTestCase has all tests of the Person Model for the app.
    """
    def setUp(self):
        # """
        #     SetUp de Test Data
        # """
        # Person.objects.create(name="Tester", last_name="1")
        Persona_De_Conectate.objects.create(nombre="Leonardo", perfil="Desarrollador Web")

    def test_nombre(self):
        """
        Test: Test Full Name
        Check the full name of a person
        """
        tester1 = Persona_De_Conectate.objects.get(id=1)
        self.assertEqual(tester1.nombre, 'Leonardo')

    def test_perfil(self):
        """
        Test: Test Full Name
        Check the full name of a person
        """
        tester1 = Persona_De_Conectate.objects.get(id=1)
        self.assertEqual(tester1.perfil, 'Desarrollador Web')
