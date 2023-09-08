import unittest
from faker import Faker

from src.logica.LogicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine
from src.modelo.ejercicio import Ejercicio

class LogicaEnFormaTestCase(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

        self.logica = LogicaEnForma()

        self.session = Session()
        self.data_faker = Faker()

        self.ejercicios_data = []
        self.ejercicios_data.append((
            "Salto Lazo",
            "Saltar y saltar",
            "https://www.youtube.com/watch?v=bmNGEzHi4-s",
            20,
        ))

        '''Se crea ejericio base'''
        self.session.add(Ejercicio(
            nombre=self.ejercicios_data[0][0],
            descripcion=self.ejercicios_data[0][1],
            enlaceYoutube=self.ejercicios_data[0][2],
            caloriasPorRepeticion=int(self.ejercicios_data[0][3]),
        ))

        for i in range(0,5):
            self.ejercicios_data.append((
                self.data_faker.unique.name(),
                self.data_faker.text(max_nb_chars=250),
                "https://www.youtube.com/watch?" + self.data_faker.name(),
                self.data_faker.random_int(10, 1000),
            ))
            self.session.add(Ejercicio(
                nombre=self.ejercicios_data[i+1][0],
                descripcion=self.ejercicios_data[i+1][1],
                enlaceYoutube=self.ejercicios_data[i+1][2],
                caloriasPorRepeticion=int(self.ejercicios_data[i+1][3]),
            ))

        self.ejercicios_data_sorted = sorted(self.ejercicios_data, key=lambda ejercicio: ejercicio[0])

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

    def test_validar_ejercicio_exitoso(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Bupies", "Salto y Flexion",
                                                               "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)
        self.assertEqual(resultado, "")

    def test_crear_ejercicio(self):
        self.logica.crear_ejercicio("Burpies", "Salto y Flexion", "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)

        ejercicio =  self.session.query(Ejercicio).filter(Ejercicio.nombre == "Burpies").first()
        self.assertEqual(ejercicio.nombre, "Burpies")
        self.assertEqual(ejercicio.descripcion, "Salto y Flexion")
        self.assertEqual(ejercicio.enlaceYoutube, "https://www.youtube.com/watch?v=bmNGEzHi4-s")
        self.assertEqual(ejercicio.caloriasPorRepeticion, 10)

    def test_listar_ejercicios(self):
        ejercicios = self.logica.dar_ejercicios()
        self.assertEqual(len(ejercicios), 6)

    def test_listar_ejercicios_ordernados_por_nombre_asc(self):
        ejercicios = self.logica.dar_ejercicios()
        for ejercicio, data_sorted in zip(ejercicios, self.ejercicios_data_sorted):
            self.assertEqual(data_sorted[0], ejercicio.nombre)
            self.assertEqual(data_sorted[1], ejercicio.descripcion)
            self.assertEqual(data_sorted[2], ejercicio.enlaceYoutube)
            self.assertEqual(data_sorted[3], ejercicio.caloriasPorRepeticion)
        self.assertEqual(len(ejercicios), 6)
