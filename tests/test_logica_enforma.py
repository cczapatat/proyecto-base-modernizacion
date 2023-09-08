import unittest

from src.logica.LogicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session
from src.modelo.ejercicio import Ejercicio

class LogicaEnFormaTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaEnForma()

        self.session = Session()

        '''Se crea ejericio base'''
        ejercicio = Ejercicio(
            nombre="Salto Lazo",
            descripcion="Saltar y saltar",
            enlaceYoutube="https://www.youtube.com/watch?v=bmNGEzHi4-s",
            caloriasPorRepeticion=20,
        )
        self.session.add(ejercicio)
        self.session.commit()

    def tearDown(self):
        self.logica = None

        self.session = Session()

        ejercicios = self.session.query(Ejercicio).all()

        for ejercicio in ejercicios:
            self.session.delete(ejercicio)

        self.session.commit()
        self.session.close()

    def test_validar_ejercicio_nombre_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("", "", "", 0)
        self.assertEqual(resultado, "Error, el campo nombre esta vacio")

    def test_validar_ejercicio_nombre_superar_longitud(self):
        resultado = self.logica.validar_crear_editar_ejercicio(41*"Z", "", "", 0)
        self.assertEqual(resultado, "Error, el campo nombre supera los 40 caracteres")

    def test_validar_ejercicio_descripcion_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "", "", 0)
        self.assertEqual(resultado, "Error, el campo descripcion esta vacio")

    def test_validar_ejercicio_descripcion_supera_longitud(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", 51*"Salto", "", 0)
        self.assertEqual(resultado, "Error, el campo descripcion supera los 250 caracteres")

    def test_validar_ejercicio_enlace_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "", 0)
        self.assertEqual(resultado, "Error, el campo enlace esta vacio")

    def test_validar_ejercicio_enlace_incorrecto(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "incorrecto", 0)
        self.assertEqual(resultado, "Error, el campo enlace es incorrecto")

    def test_validar_ejercicio_enlace_no_es_youtube(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "https://google.com/any", 0)
        self.assertEqual(resultado, "Error, el campo enlace no es de Youtube")

    def test_validar_ejercicio_calorias_incorrectas(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "https://www.youtube.com/watch?v=bmNGEzHi4-s", "")
        self.assertEqual(resultado, "Error, el campo calorias debe ser un número entero")

    def test_validar_ejercicio_calorias_no_es_mayor_a_cero(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "https://www.youtube.com/watch?v=bmNGEzHi4-s", -1)
        self.assertEqual(resultado, "Error, el campo calorias debe ser mayor a cero")

    def test_validar_ejercicio_nombre_duplicado(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Salto Lazo", "Saltar 15 veces", "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)
        self.assertEqual(resultado, "Error, el ejericio Salto Lazo ya existe")
