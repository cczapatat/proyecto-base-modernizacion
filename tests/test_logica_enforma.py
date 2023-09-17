import datetime
import unittest
from faker import Faker
from sqlalchemy import asc, desc, func

from src.logica.LogicaEnForma import LogicaEnForma, ClasificacionIMC
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

        self.id_persona_entrenando = 0

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
                self.data_faker.random_int(1, 2),
                self.data_faker.random_int(70, 100),
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
                fecha_retiro="",
                talla=self.personas_data[i][2],
                peso=self.personas_data[i][3],
                edad=self.personas_data[i][4],
                brazo=self.personas_data[i][5],
                pierna=self.personas_data[i][6],
                pecho=self.personas_data[i][7],
                cintura=self.personas_data[i][8],
            ))

        self.personas_data_sorted = sorted(self.personas_data, key=lambda persona: persona[0])

    def agregar_persona(self, nombre, talla, peso):
        persona = Persona(
            nombre=nombre,
            apellido="N/A",
            fecha_inicio=datetime.date.today().strftime("%Y-%m-%d"),
            talla=talla,
            peso=peso,
            edad=self.data_faker.random_int(10, 100),
            brazo=self.data_faker.random_int(10, 100),
            pierna=self.data_faker.random_int(10, 100),
            pecho=self.data_faker.random_int(10, 100),
            cintura=self.data_faker.random_int(10, 100),
        )
        self.session.add(persona)
        self.session.commit()

        self.personas_data_sorted.append((
            persona.nombre,
            persona.apellido,
            persona.talla,
            persona.peso,
            persona.edad,
            persona.brazo,
            persona.pierna,
            persona.pecho,
            persona.cintura,
        ))
        self.personas_data_sorted = sorted(self.personas_data_sorted, key=lambda persona: persona[0])

        id_persona = self.personas_data_sorted.index(
            next(filter(lambda item: item[0] == persona.nombre, self.personas_data_sorted))
        )

        return {"persona": persona, "id_persona": id_persona}

    def init_entrenamientos(self):
        self.entrenamientos_data = []
        ejercicios = self.session.query(Ejercicio).order_by(asc("nombre")).limit(10).all()
        self.personaEntrenando = (self.session.query(Persona)
                                  .filter(Persona.nombre == self.personas_data_sorted[self.id_persona_entrenando][0])
                                  .first())

        for i in range(0, len(ejercicios)):
            value = i + 1
            if value < 10:
                index = "0{}".format(value)
            else:
                index = value
            fechaStr = "2023-0{}-{}".format(self.data_faker.random_int(1, 9), index)
            fechaDate = datetime.datetime.strptime(fechaStr, "%Y-%m-%d")

            self.entrenamientos_data.append((
                self.personaEntrenando.id,  # 0
                ejercicios[i].id,  # 1
                ejercicios[i].nombre,
                fechaStr,  # 3
                fechaDate,
                self.data_faker.random_int(10, 1000),  # 5
                "{}:{}:{}".format(self.data_faker.random_int(0, 2), self.data_faker.random_int(0, 59),
                                  self.data_faker.random_int(1, 59)),  # 6
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

    def crear_entrenamientos(self, id_persona):
        ejercicios = self.session.query(Ejercicio).order_by(asc("nombre")).limit(10).all()
        entrenados = []

        total_calorias = 0
        total_repeticiones = 0

        for i in range(0, len(ejercicios)):
            entrenado = EjercicioEntrenado(
                persona_id=id_persona,
                ejercicio_id=ejercicios[i].id,
                fecha=self.data_faker.random_choices(elements=('2023-09-10', '2023-09-11', '2023-09-12'), length=1)[0],
                repeticiones=self.data_faker.random_int(10, 300),
                tiempo="00:10:00",
            )
            entrenados.append(entrenado)
            self.session.add(entrenado)
            self.session.commit()

        historial = (self.session.query(
            EjercicioEntrenado,
            func.sum(EjercicioEntrenado.repeticiones),
            func.sum(EjercicioEntrenado.repeticiones * Ejercicio.calorias),
        )
                     .join(Ejercicio, EjercicioEntrenado.ejercicio_id == Ejercicio.id)
                     .filter(EjercicioEntrenado.persona_id == id_persona)
                     .group_by("fecha").order_by(desc("fecha")).all())

        for item in historial:
            total_repeticiones += item[1]
            total_calorias += item[2]

        return {
            "historial": historial,
            "total_calorias": total_calorias,
            "total_repeticiones": total_repeticiones,
        }

    def tearDown(self):
        self.logica = None

        self.session = Session()

        ejerciciosEntrenados = self.session.query(EjercicioEntrenado).all()

        for ejercicioEntrenado in ejerciciosEntrenados:
            self.session.delete(ejercicioEntrenado)

        ejercicios = self.session.query(Ejercicio).all()

        for ejercicio in ejercicios:
            self.session.delete(ejercicio)

        personas = self.session.query(Persona).all()

        for persona in personas:
            self.session.delete(persona)

        self.session.commit()
        self.session.close()

    def obtener_persona_crear_entrenamiento(self):
        id_persona = 0
        return self.session.query(Persona).filter(Persona.nombre == self.personas_data_sorted[id_persona][0]).first()

    def obtener_ejercicio_crear_entrenamiento(self):
        return self.session.query(Ejercicio).first()

    def test_validar_ejercicio_nombre_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("", "", "", 0)
        self.assertEqual(resultado, "Error, el campo nombre esta vacio")

    def test_validar_ejercicio_nombre_superar_longitud(self):
        resultado = self.logica.validar_crear_editar_ejercicio(41 * "Z", "", "", 0)
        self.assertEqual(resultado, "Error, el campo nombre supera los 40 caracteres")

    def test_validar_ejercicio_descripcion_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "", "", 0)
        self.assertEqual(resultado, "Error, el campo descripcion esta vacio")

    def test_validar_ejercicio_descripcion_supera_longitud(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", 51 * "Salto", "", 0)
        self.assertEqual(resultado, "Error, el campo descripcion supera los 250 caracteres")

    def test_validar_ejercicio_enlace_vacio(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "", 0)
        self.assertEqual(resultado, "Error, el campo enlace esta vacio")

    def test_validar_ejercicio_enlace_incorrecto(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "incorrecto", 0)
        self.assertEqual(resultado, "Error, el campo enlace es incorrecto")

    def test_validar_ejercicio_enlace_no_es_youtube(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion", "https://google.com/any",
                                                               0)
        self.assertEqual(resultado, "Error, el campo enlace no es de Youtube")

    def test_validar_ejercicio_calorias_incorrectas(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion",
                                                               "https://www.youtube.com/watch?v=bmNGEzHi4-s", "")
        self.assertEqual(resultado, "Error, el campo calorias debe ser un número entero")

    def test_validar_ejercicio_calorias_no_es_mayor_a_cero(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Burpies", "Salto y Flexion",
                                                               "https://www.youtube.com/watch?v=bmNGEzHi4-s", -1)
        self.assertEqual(resultado, "Error, el campo calorias debe ser mayor a cero")

    def test_validar_ejercicio_nombre_duplicado(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Salto Lazo", "Saltar 15 veces",
                                                               "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)
        self.assertEqual(resultado, "Error, el ejericio Salto Lazo ya existe")

    def test_validar_ejercicio_exitoso(self):
        resultado = self.logica.validar_crear_editar_ejercicio("Bupies", "Salto y Flexion",
                                                               "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)
        self.assertEqual(resultado, "")

    def test_crear_ejercicio(self):
        self.logica.crear_ejercicio("Burpies", "Salto y Flexion", "https://www.youtube.com/watch?v=bmNGEzHi4-s", 10)

        ejercicio = self.session.query(Ejercicio).filter(Ejercicio.nombre == "Burpies").first().__dict__
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
        ejerciciosEntrenados = self.logica.dar_entrenamientos(self.id_persona_entrenando)
        self.assertEqual(len(ejerciciosEntrenados), len(self.entrenamientos_data))

    def test_listar_entrenamientos_de_una_persona_ordenados(self):
        ejerciciosEntrenados = self.logica.dar_entrenamientos(self.id_persona_entrenando)
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

    def test_validar_entrenamiento_diccionario_persona_vacio(self):
        resultado = self.logica.validar_crear_editar_entrenamiento({}, "", "", "", "")
        self.assertEqual(resultado, "Error, el diccionario persona esta vacio")

    def test_validar_entrenamiento_ejercicio_vacio(self):
        persona = self.obtener_persona_crear_entrenamiento()
        resultado = self.logica.validar_crear_editar_entrenamiento(persona, "", "", "", "")
        self.assertEqual(resultado, "Error, el campo ejercicio esta vacio")

    def test_validar_entrenamiento_fecha_vacio(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "", "", "")
        self.assertEqual(resultado, "Error, el campo fecha esta vacio")

    def test_validar_entrenamiento_fecha_formato_no_valido(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "fecha-erronea",
                                                                   "", "")
        self.assertEqual(resultado, "Error, la fecha no es valida. Debe tener formato YYYY-MM-DD")

    def test_validar_entrenamiento_fecha_no_valida(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2026-09-09", "",
                                                                   "")
        self.assertEqual(resultado, "Error, la fecha ingresada debe ser igual o menor al dia de hoy")

    def test_validar_entrenamiento_repeticiones_no_valido(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09", "",
                                                                   "")
        self.assertEqual(resultado, "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero")

    def test_validar_entrenamiento_repeticiones_numero_no_valido(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09",
                                                                   "-1", "")
        self.assertEqual(resultado, "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero")

    def test_validar_entrenamiento_tiempo_vacio(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09",
                                                                   "10", "")
        self.assertEqual(resultado, "Error, el tiempo esta vacio")

    def test_validar_entrenamiento_tiempo_formato_no_valido(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09",
                                                                   "10", "tiempo_mal_formateado")
        self.assertEqual(resultado, "Error, el tiempo no es valida. Debe tener formato hh:mm:ss")

    def test_validar_entrenamiento_datos_validos(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()

        resultado = self.logica.validar_crear_editar_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09",
                                                                   "10", "00:10:00")
        self.assertEqual(resultado, "")

    def test_crear_entrenamiento(self):
        persona = self.obtener_persona_crear_entrenamiento()
        ejercicio = self.obtener_ejercicio_crear_entrenamiento()
        self.logica.crear_entrenamiento(persona.__dict__, ejercicio.nombre, "2022-09-09",
                                        "10", "00:10:00")

        entrenamiento = self.session.query(EjercicioEntrenado).filter(
            EjercicioEntrenado.persona_id == persona.id,
            EjercicioEntrenado.ejercicio_id == ejercicio.id
        ).order_by(desc("id")).first().__dict__

        self.assertEqual(entrenamiento["fecha"], "2022-09-09")
        self.assertEqual(entrenamiento["repeticiones"], 10)
        self.assertEqual(entrenamiento["tiempo"], "00:10:00")

    def test_generar_report_persona_sin_entrenamientos(self):
        index = len(self.personas_data_sorted) - 1
        reporte = self.logica.dar_reporte(index)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), 0)
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 0)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 0)
        self.assertEqual(reporte["persona"]["nombre"], self.personas_data_sorted[index][0])
        self.assertEqual(reporte["persona"]["talla"], self.personas_data_sorted[index][2])
        self.assertEqual(reporte["persona"]["peso"], self.personas_data_sorted[index][3])

    def test_generar_reporte_imc_bajo_peso_persona_sin_entrenamientos(self):
        nuevo_registro = self.agregar_persona("flaco", 1.8, 55)
        persona = nuevo_registro["persona"]
        imc = persona.peso / (pow(persona.talla, 2))
        id_persona = nuevo_registro["id_persona"]

        reporte = self.logica.dar_reporte(id_persona)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), 0)
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 0)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 0)
        self.assertEqual(reporte["estadisticas"]["imc"], imc)
        self.assertEqual(reporte["estadisticas"]["clasificacion"], ClasificacionIMC.BAJO_PESO.value)
        self.assertEqual(reporte["persona"]["nombre"], persona.nombre)
        self.assertEqual(reporte["persona"]["talla"], persona.talla)
        self.assertEqual(reporte["persona"]["peso"], persona.peso)

    def test_generar_reporte_imc_peso_saludable_persona_sin_entrenamientos(self):
        nuevo_registro = self.agregar_persona("bien", 1.8, 70)
        persona = nuevo_registro["persona"]
        imc = persona.peso / (pow(persona.talla, 2))
        id_persona = nuevo_registro["id_persona"]

        reporte = self.logica.dar_reporte(id_persona)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), 0)
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 0)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 0)
        self.assertEqual(reporte["estadisticas"]["imc"], imc)
        self.assertEqual(reporte["estadisticas"]["clasificacion"], ClasificacionIMC.PESO_SALUDABLE.value)
        self.assertEqual(reporte["persona"]["nombre"], persona.nombre)
        self.assertEqual(reporte["persona"]["talla"], persona.talla)
        self.assertEqual(reporte["persona"]["peso"], persona.peso)

    def test_generar_reporte_imc__persona_sin_entrenamientos(self):
        nuevo_registro = self.agregar_persona("mal", 1.7, 75)
        persona = nuevo_registro["persona"]
        imc = persona.peso / (pow(persona.talla, 2))
        id_persona = nuevo_registro["id_persona"]

        reporte = self.logica.dar_reporte(id_persona)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), 0)
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 0)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 0)
        self.assertEqual(reporte["estadisticas"]["imc"], imc)
        self.assertEqual(reporte["estadisticas"]["clasificacion"], ClasificacionIMC.SOBREPESO.value)
        self.assertEqual(reporte["persona"]["nombre"], persona.nombre)
        self.assertEqual(reporte["persona"]["talla"], persona.talla)
        self.assertEqual(reporte["persona"]["peso"], persona.peso)

    def test_generar_reporte_imc_obesidad_persona_sin_entrenamientos(self):
        nuevo_registro = self.agregar_persona("hiper_mal", 1.7, 100)
        persona = nuevo_registro["persona"]
        imc = persona.peso / (pow(persona.talla, 2))
        id_persona = nuevo_registro["id_persona"]

        reporte = self.logica.dar_reporte(id_persona)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), 0)
        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], 0)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], 0)
        self.assertEqual(reporte["estadisticas"]["imc"], imc)
        self.assertEqual(reporte["estadisticas"]["clasificacion"], ClasificacionIMC.OBESIDAD.value)
        self.assertEqual(reporte["persona"]["nombre"], persona.nombre)
        self.assertEqual(reporte["persona"]["talla"], persona.talla)
        self.assertEqual(reporte["persona"]["peso"], persona.peso)

    def test_generar_reporte_persona_con_entrenamientos(self):
        nuevo_registro = self.agregar_persona("pepito", 1.7, 70)
        persona = nuevo_registro["persona"]
        imc = persona.peso / (pow(persona.talla, 2))
        id_persona = nuevo_registro["id_persona"]

        rutina = self.crear_entrenamientos(persona.id)
        historial = rutina["historial"]
        total_calorias = rutina["total_calorias"]
        total_repeticiones = rutina["total_repeticiones"]

        reporte = self.logica.dar_reporte(id_persona)
        self.assertEqual(len(reporte["estadisticas"]["entrenamientos"]), len(historial))
        for i in range(0, len(historial)):
            self.assertEqual(reporte["estadisticas"]["entrenamientos"][i]["fecha"], historial[i][0].fecha)
            self.assertEqual(reporte["estadisticas"]["entrenamientos"][i]["repeticiones"], historial[i][1])
            self.assertEqual(reporte["estadisticas"]["entrenamientos"][i]["calorias"], historial[i][2])

        self.assertEqual(reporte["estadisticas"]["total_repeticiones"], total_repeticiones)
        self.assertEqual(reporte["estadisticas"]["total_calorias"], total_calorias)
        self.assertEqual(reporte["estadisticas"]["imc"], imc)
        self.assertEqual(reporte["estadisticas"]["clasificacion"], ClasificacionIMC.PESO_SALUDABLE.value)
        self.assertEqual(reporte["persona"]["nombre"], persona.nombre)
        self.assertEqual(reporte["persona"]["talla"], persona.talla)
        self.assertEqual(reporte["persona"]["peso"], persona.peso)
