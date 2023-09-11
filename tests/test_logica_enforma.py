import datetime
import unittest
from faker import Faker
from sqlalchemy import asc

from src.logica.LogicaEnForma import LogicaEnForma
from src.modelo.declarative_base import Session, Base, engine
from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.modelo.ejercicioEntrenado import EjercicioEntrenado

class LogicaEnFormaTestCase(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

        self.logica = LogicaEnForma()

        self.session = Session()
        self.data_faker = Faker()

        self.init_ejercicios()
        self.init_personas()

        self.session.commit()

        self.persona_entrenando = self.session.query(Persona).order_by(asc("nombre")).first().__dict__

        self.init_entrenamientos()
        self.session.commit()

    def init_ejercicios(self):
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
            youtube=self.ejercicios_data[0][2],
            calorias=int(self.ejercicios_data[0][3]),
        ))

        for i in range(0, 5):
            self.ejercicios_data.append((
                self.data_faker.unique.name(),
                self.data_faker.text(max_nb_chars=250),
                "https://www.youtube.com/watch?" + self.data_faker.name(),
                self.data_faker.random_int(10, 1000),
            ))
            self.session.add(Ejercicio(
                nombre=self.ejercicios_data[i + 1][0],
                descripcion=self.ejercicios_data[i + 1][1],
                youtube=self.ejercicios_data[i + 1][2],
                calorias=int(self.ejercicios_data[i + 1][3]),
            ))

        self.ejercicios_data_sorted = sorted(self.ejercicios_data, key=lambda ejercicio: ejercicio[0])

    def init_personas(self):
        self.personas_data = []

        for i in range(0, 5):
            self.personas_data.append((
                self.data_faker.unique.first_name(),
                self.data_faker.unique.last_name(),
                self.data_faker.random_int(10, 1000),
                self.data_faker.random_int(10, 1000),
                self.data_faker.random_int(10, 100),
                self.data_faker.random_int(10, 1000),
                self.data_faker.random_int(10, 1000),
                self.data_faker.random_int(10, 1000),
                self.data_faker.random_int(10, 1000),
            ))
            self.session.add(Persona(
                nombre=self.personas_data[i][0],
                apellido=self.personas_data[i][1],
                fecha_inicio=datetime.date.today().strftime("%Y-%m-%d"),
                talla=self.personas_data[i][2],
                peso=self.personas_data[i][3],
                edad=self.personas_data[i][4],
                brazo=self.personas_data[i][5],
                pierna=self.personas_data[i][6],
                pecho=self.personas_data[i][7],
                cintura=self.personas_data[i][8],
            ))

        self.personas_data_sorted = sorted(self.personas_data, key=lambda persona: persona[0])

    def init_entrenamientos(self):
        self.entrenamientos_data = []
        ejercicios = self.session.query(Ejercicio).order_by(asc("nombre")).limit(10).all()

        for i in range(0, len(ejercicios)):
            value = i + 1
            if value < 10:
                index = "0{}".format(value)
            else:
                index = value
            fechaStr = "2023-0{}-{}".format(self.data_faker.random_int(1, 9), index)
            fechaDate = datetime.datetime.strptime(fechaStr, "%Y-%m-%d")

            self.entrenamientos_data.append((
                self.persona_entrenando["id"], # 0
                ejercicios[i].id, # 1
                ejercicios[i].nombre,
                fechaStr, # 3
                fechaDate,
                self.data_faker.random_int(10, 1000), # 5
                "{}:{}:{}".format(self.data_faker.random_int(0, 2), self.data_faker.random_int(0, 59), self.data_faker.random_int(1, 59)), # 6
            ))
            self.session.add(EjercicioEntrenado(
                persona_id=self.entrenamientos_data[i][0],
                ejercicio_id=self.entrenamientos_data[i][1],
                fecha=self.entrenamientos_data[i][3],
                repeticiones=self.entrenamientos_data[i][5],
                tiempo=self.entrenamientos_data[i][6],
            ))

        self.entrenamientos_data_sorted = sorted(
            self.entrenamientos_data,
            key=lambda entrenamiento: (entrenamiento[3], entrenamiento[2]),
            reverse=True,
        )

    def tearDown(self):
        self.logica = None

        self.session = Session()

        ejercicios = self.session.query(Ejercicio).all()

        for ejercicio in ejercicios:
            self.session.delete(ejercicio)

        personas = self.session.query(Persona).all()

        for persona in personas:
            self.session.delete(persona)

        ejerciciosEntrenados = self.session.query(EjercicioEntrenado).all()

        for ejercicioEntrenado in ejerciciosEntrenados:
            self.session.delete(ejercicioEntrenado)

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

        ejercicio =  self.session.query(Ejercicio).filter(Ejercicio.nombre == "Burpies").first().__dict__
        self.assertEqual(ejercicio["nombre"], "Burpies")
        self.assertEqual(ejercicio["descripcion"], "Salto y Flexion")
        self.assertEqual(ejercicio["youtube"], "https://www.youtube.com/watch?v=bmNGEzHi4-s")
        self.assertEqual(ejercicio["calorias"], 10)

    def test_listar_ejercicios(self):
        ejercicios = self.logica.dar_ejercicios()
        self.assertEqual(len(ejercicios), 6)

    def test_listar_ejercicios_ordernados_por_nombre_asc(self):
        ejercicios = self.logica.dar_ejercicios()
        for ejercicio, data_sorted in zip(ejercicios, self.ejercicios_data_sorted):
            self.assertEqual(data_sorted[0], ejercicio["nombre"])
            self.assertEqual(data_sorted[1], ejercicio["descripcion"])
            self.assertEqual(data_sorted[2], ejercicio["youtube"])
            self.assertEqual(data_sorted[3], ejercicio["calorias"])
        self.assertEqual(len(ejercicios), 6)

    def test_listar_personas(self):
        personas = self.logica.dar_personas()
        self.assertEqual(len(personas), 5)

    def test_listar_personas_ordernados_por_nombre_asc(self):
        personas = self.logica.dar_personas()
        for persona, data_sorted in zip(personas, self.personas_data_sorted):
            self.assertEqual(data_sorted[0], persona["nombre"])
            self.assertEqual(data_sorted[1], persona["apellido"])
            self.assertEqual(data_sorted[2], persona["talla"])
            self.assertEqual(data_sorted[3], persona["peso"])
            self.assertEqual(data_sorted[4], persona["edad"])
            self.assertEqual(data_sorted[5], persona["brazo"])
            self.assertEqual(data_sorted[6], persona["pierna"])
            self.assertEqual(data_sorted[7], persona["pecho"])
            self.assertEqual(data_sorted[8], persona["cintura"])
        self.assertEqual(len(personas), 5)

    def test_lista_entrenamientos_de_una_persona_incorrect(self):
        ejerciciosEntrenados = self.logica.dar_entrenamientos(-1)
        self.assertEqual(len(ejerciciosEntrenados), 0)

    def test_listar_entrenamientos_de_una_persona(self):
        ejerciciosEntrenados = self.logica.dar_entrenamientos(self.persona_entrenando["id"])
        self.assertEqual(len(ejerciciosEntrenados), len(self.entrenamientos_data))

    def test_listar_entrenamientos_de_una_persona_ordenados(self):
        ejerciciosEntrenados = self.logica.dar_entrenamientos(self.persona_entrenando["id"])
        for ejercicioEntrenado, data_sorted in zip(ejerciciosEntrenados, self.entrenamientos_data_sorted):
            self.assertEqual(data_sorted[2], ejercicioEntrenado["ejercicio"])
            self.assertEqual(data_sorted[3], ejercicioEntrenado["fecha"])
            self.assertEqual(data_sorted[5], ejercicioEntrenado["repeticiones"])
            self.assertEqual(data_sorted[6], ejercicioEntrenado["tiempo"])
        self.assertEqual(len(ejerciciosEntrenados), len(self.entrenamientos_data))

    def test_dar_persona(self):
        id_persona = 0
        persona = self.session.query(Persona).filter(Persona.nombre == self.personas_data_sorted[id_persona][0]).first()
        result = self.logica.dar_persona(id_persona)
        self.assertEqual(persona.nombre, result["nombre"])
        self.assertEqual(persona.apellido, result["apellido"])