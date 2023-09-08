import unittest

from src.logica.LogicaEnForma import LogicaEnForma

class LogicaEnFormaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaEnForma()

    def tearDown(self):
        self.logica = None

    def test_validar_ejercicio_nombre_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("", "", "", 0)
        self.assertEqual(resultado, "Error, el campo nombre esta vacio")

    def test_validar_ejercicio_descripcion_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "", "", 0)
        self.assertEqual(resultado, "Error, el campo descripcion esta vacio")

    def test_validar_ejercicio_enlace_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "", 0)
        self.assertEqual(resultado, "Error, el campo enlace esta vacio")