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
        txt_usuario = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "id_usuario")))
        txt_usuario.clear()
        txt_usuario.send_keys(usuario)
        password = self.browser.find_element_by_id("id_contrasenia")
        password.clear()
        password.send_keys(contrasenia)
        btn = self.browser.find_element_by_id("btn-submit-login")
        btn.click()
        self.browser.implicitly_wait(5)

    # Verifica la funcionalidad de login y logout
    # Casos de prueba:
    # 1. Se ingresa un usuario y contraseña invalidos.
    # 2. Se ingresa un usuario y contraseña validos.
    # 3. Se cierra la sesión del usuario
    def test_login_logout(self):
        self.browser.get(base_url)
        self.browser.find_element_by_id("btn-login").click()
        self.browser.implicitly_wait(5)

        # ----------------------------------------------------
        # Caso de prueba 1
        # ----------------------------------------------------

        self.iniciar_sesion("admin", "Colombia.2017")

        assert self.is_element_present(By.CLASS_NAME, 'is-invalid', 10)

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

        assert not self.is_element_present(By.CSS_SELECTOR, '#btn-user', 10)
        assert self.is_element_present(By.CSS_SELECTOR, '#btn-login', 5)
        btn_login = self.browser.find_element_by_css_selector('#btn-login')
        btn_login.click()

        assert self.is_element_present(By.ID, "id_usuario", 5)
        assert self.is_element_present(By.ID, "id_contrasenia", 5)
        assert self.is_element_present(By.ID, "btn-submit-login", 5)

    # Verifica la funcionalidad de registro (CON-158)
    # Casos de prueba:
    # 1. Prueba el registro con datos inválidos
    # 2. Prueba el registro con datos validos
    # 3. Verifica que no se pueda registrar nuevamente
    def test_registro(self):
        self.browser.get(base_url+'/ingresar')

        first_name = getRandomString(10)
        last_name = getRandomString(10)
        username = getRandomString(10)
        contrasenia = getRandomString(10)

        # 1. Datos inválidos
        txt_contrasenia1 = self.browser.find_element_by_id("id_password1")
        txt_contrasenia2 = self.browser.find_element_by_id("id_password2")
        txt_username = self.browser.find_element_by_id("usuario_reg")
        txt_first_name = self.browser.find_element_by_id("id_first_name")
        txt_last_name = self.browser.find_element_by_id("id_last_name")
        cb_terminos = self.browser.find_element_by_id('id_terminos')
        btn_registrar = self.browser.find_element_by_id('btn-registrar')

        cb_terminos.click()
        txt_contrasenia1.send_keys("123456789")
        txt_contrasenia2.send_keys("123456789")
        txt_username.send_keys('prueba@conectate.co')
        txt_first_name.send_keys(first_name)
        txt_last_name.send_keys(last_name)

        btn_registrar.click()

        assert self.is_element_present(By.CLASS_NAME, 'is-invalid', 5)
        assert self.is_element_present(By.CLASS_NAME, 'invalid-feedback', 5)
        assert self.is_element_present(By.CLASS_NAME, 'is-valid', 5)
        assert len(self.browser.find_elements_by_css_selector('.reg-field .is-invalid')) == 3
        assert len(self.browser.find_elements_by_class_name('invalid-feedback')) == 2
        assert len(self.browser.find_elements_by_class_name('is-valid')) == 2

        # 2. datos válidos
        txt_contrasenia1 = self.browser.find_element_by_id("id_password1")
        txt_contrasenia2 = self.browser.find_element_by_id("id_password2")
        txt_username = self.browser.find_element_by_id("usuario_reg")
        btn_registrar = self.browser.find_element_by_id('btn-registrar')

        txt_contrasenia1.clear()
        txt_contrasenia2.clear()
        txt_username.clear()

        txt_contrasenia1.send_keys(contrasenia)
        txt_contrasenia2.send_keys(contrasenia)
        txt_username.send_keys(username)

        btn_registrar.click()

        assert self.is_element_present(By.CSS_SELECTOR, '.toast-success', 5)
        self.browser.find_element_by_css_selector(".toast-close-button").click()
        assert not self.is_element_present(By.ID, 'error-alert', 5)
        assert self.is_element_present(By.ID, 'btn-user', 5)
        btn_user = self.browser.find_element_by_css_selector('#btn-user ')
        assert btn_user.text == username+'@uniandes.edu.co'

        btn_user.click()
        self.browser.get(base_url+'/auth/logout')

        self.browser.get(base_url+'/ingresar')

        # 3. Probar que no se pueda volver a registrar

        txt_contrasenia1 = self.browser.find_element_by_id("id_password1")
        txt_contrasenia2 = self.browser.find_element_by_id("id_password2")
        txt_username = self.browser.find_element_by_id("usuario_reg")
        txt_first_name = self.browser.find_element_by_id("id_first_name")
        txt_last_name = self.browser.find_element_by_id("id_last_name")
        cb_terminos = self.browser.find_element_by_id('id_terminos')
        btn_registrar = self.browser.find_element_by_id('btn-registrar')

        txt_username.send_keys(username+'@uniandes.edu.co')
        txt_contrasenia1.send_keys(contrasenia)
        txt_contrasenia2.send_keys(contrasenia)
        txt_first_name.send_keys(first_name)
        txt_last_name.send_keys(last_name)
        cb_terminos.click()

        btn_registrar.click()

        assert self.is_element_present(By.CLASS_NAME, 'is-invalid', 5)
        assert self.is_element_present(By.CLASS_NAME, 'invalid-feedback', 5)
        assert self.is_element_present(By.CLASS_NAME, 'is-valid', 5)
        assert len(self.browser.find_elements_by_css_selector('.reg-field .is-invalid')) == 1
        assert len(self.browser.find_elements_by_class_name('invalid-feedback')) == 1
        assert len(self.browser.find_elements_by_class_name('is-valid')) == 2