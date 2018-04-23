from unittest import TestCase

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import random
from selenium.webdriver.support import expected_conditions as EC
import string

from selenium.webdriver.support.wait import WebDriverWait


def getRandomString(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def getRealPath(rel_path):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, rel_path)
    return os.path.realpath(abs_file_path)


base_url = 'http://localhost:8000'


class FunctionalTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(getRealPath('../TDD/chromedriver'))
        self.browser.set_window_size(1024, 786)
        self.browser.implicitly_wait(2)

    def is_element_present(self, how, what, timeout):
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
            return element.is_displayed()
        except Exception as e:
            return False

    def tearDown(self):
        self.browser.quit()

    def iniciar_sesion(self, usuario, contrasenia):
        txt_usuario = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "id_user")))
        txt_usuario.clear()
        txt_usuario.send_keys(usuario)
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(contrasenia)
        self.browser.find_element_by_id("btn-ingresar").click()
        self.browser.implicitly_wait(5)

    # Verifica la funcionalidad de login y logout
    # Casos de prueba:
    # 1. Se ingresa un usuario y contraseña invalidos.
    # 2. Se ingresa un usuario y contraseña validos.
    # 3. Se cierra la sesión del usuario
    def test_CON53(self):
        self.browser.get(base_url)
        self.browser.find_element_by_id("btn-login").click()
        self.browser.implicitly_wait(5)

        # ----------------------------------------------------
        # Caso de prueba 1
        # ----------------------------------------------------

        self.iniciar_sesion("admin", "Colombia.2017")

        assert self.is_element_present(By.ID, 'error-alert', 10)

        # ----------------------------------------------------
        # Caso de prueba 2
        # ----------------------------------------------------

        self.iniciar_sesion("admin", "Colombia.2018")
        self.browser.implicitly_wait(5)

        assert self.is_element_present(By.CSS_SELECTOR, '.toast-success', 5)
        self.browser.find_element_by_css_selector(".toast-close-button").click()
        assert not self.is_element_present(By.ID, 'error-alert', 5)
        assert self.is_element_present(By.ID, 'btn-user', 5)

        btn_user = self.browser.find_element_by_css_selector('#btn-user ')
        assert btn_user.text == 'admin@conectate.co'
        btn_user.click()

        assert self.is_element_present(By.ID, 'link-historial', 5)
        assert self.is_element_present(By.ID, 'link-perfil', 5)
        assert self.is_element_present(By.ID, 'link-logout', 5)

        # ----------------------------------------------------
        # Caso de prueba 3
        # ----------------------------------------------------

        btn_logout = self.browser.find_element_by_css_selector('#link-logout')
        btn_logout.click()

        assert self.is_element_present(By.ID, 'btn-login',5)

        btn_login = self.browser.find_element_by_css_selector('#btn-login')
        btn_login.click()

        assert self.is_element_present(By.ID, "id_user", 5)
        assert self.is_element_present(By.ID, "id_password", 5)
        assert self.is_element_present(By.ID, "btn-ingresar", 5)
        assert not self.is_element_present(By.ID, 'link-historial', 1)
        assert not self.is_element_present(By.ID, 'link-perfil', 1)
        assert not self.is_element_present(By.ID, 'link-logout', 1)
