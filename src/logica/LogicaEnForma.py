import datetime
import enum
import validators
import re

from sqlalchemy import asc, func, desc
from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import engine, Base, session
from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.modelo.ejercicioEntrenado import EjercicioEntrenado

class ClasificacionIMC(enum.Enum):
    BAJO_PESO = "Bajo peso"
    PESO_SALUDABLE = "Peso saludable"
    SOBREPESO = "Sobrepeso"
    OBESIDAD = "Obesidad"

class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        Base.metadata.create_all(engine)

    def es_enlace_youtube(self, enlace):
        return enlace.startswith("https://www.youtube.com/watch?")

    def dar_ejercicios_por_nombre(self, nombre_ejercicio):
        return session.query(Ejercicio).filter(Ejercicio.nombre == nombre_ejercicio).all()

    def dar_ejercicio_por_nombre(self, nombre_ejercicio):
        return session.query(Ejercicio).filter(Ejercicio.nombre == nombre_ejercicio).first()

    def mapear_none_a_vacio(self, valor):
        valor_temporal = valor

        if valor is None:
            valor_temporal = ""

        return valor_temporal

    def es_diccionario_vacio(self, dict):
        return bool(dict) is False

    def obtener_fecha_de_string(self, str_fecha, formato):
        return datetime.datetime.strptime(str_fecha, formato)


    def fecha_menor_igual_dia_actual(self, fecha):
        return fecha <= datetime.datetime.now()

    def tiempo_tiene_formato_valido(self, tiempo):
        return re.findall("\d\d:\d\d:\d\d", tiempo)

    def calcular_imc(self, peso, talla):
        return peso / pow(talla, 2)

    def calcular_clasificacion_imc(self, imc):
        if imc < 18.5:
            clasificacion = ClasificacionIMC.BAJO_PESO.value
        elif 18.5 <= imc <= 24.9:
            clasificacion = ClasificacionIMC.PESO_SALUDABLE.value
        elif 25 <= imc <= 29.9:
            clasificacion = ClasificacionIMC.SOBREPESO.value
        else:
            clasificacion = ClasificacionIMC.OBESIDAD.value

        return clasificacion

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        error = ""
        calorias_int = 0

        if not error and len(nombre) == 0:
            error = "Error, el campo nombre esta vacio"

        if not error and len(nombre) > 40:
            error = "Error, el campo nombre supera los 40 caracteres"

        if not error and len(descripcion) == 0:
            error = "Error, el campo descripcion esta vacio"

        if not error and len(descripcion) > 250:
            error = "Error, el campo descripcion supera los 250 caracteres"

        if not error and len(enlace) == 0:
            error = "Error, el campo enlace esta vacio"

        if not error and (not validators.url(enlace)):
            error = "Error, el campo enlace es incorrecto"

        if not error and not self.es_enlace_youtube(enlace):
            error = "Error, el campo enlace no es de Youtube"

        if not error:
            try:
                calorias_int = int(calorias)
            except ValueError:
                error = "Error, el campo calorias debe ser un número entero"

        if not error and calorias_int <= 0:
            error = "Error, el campo calorias debe ser mayor a cero"

        ejercicios_por_nombre = self.dar_ejercicios_por_nombre(nombre)

        if not error and len(ejercicios_por_nombre) > 0:
            error = "Error, el ejericio " + nombre + " ya existe"

        return error

    def crear_ejercicio(self, nombre, descripcion, enlace, calorias):
        ejercicio = Ejercicio(nombre=nombre, descripcion=descripcion, youtube=enlace,
                              calorias=calorias)
        session.add(ejercicio)
        session.commit()

        return True

    def dar_ejercicios(self):
        ejercicios = session.query(Ejercicio).order_by(asc("nombre")).all()
        result = []
        for ejercicio in ejercicios:
            result.append(ejercicio.__dict__)

        return result

    def dar_personas(self):
        personas = session.query(Persona).order_by(asc("nombre")).all()
        result = []
        for persona in personas:
            persona_dict = persona.__dict__
            persona_dict["fecha_retiro"] = self.mapear_none_a_vacio(persona_dict["fecha_retiro"])
            persona_dict["razon_retiro"] = self.mapear_none_a_vacio(persona_dict["razon_retiro"])

            result.append(persona_dict)

        return result

    def dar_persona(self, id_persona):
        personas = self.dar_personas()

        return personas[id_persona]

    def dar_ejercicio_entrenados_por_persona_id(self, person_id):
        return ((session.query(EjercicioEntrenado, Ejercicio)
                .join(Ejercicio, EjercicioEntrenado.ejercicio_id == Ejercicio.id))
                .filter(EjercicioEntrenado.persona_id == person_id).all())

    def mapear_objeto_entrenamiento(self, ejercicioEntrenado):
        return {
                "id": ejercicioEntrenado[0].id,
                "ejercicio_id": ejercicioEntrenado[0].ejercicio_id,
                "ejercicio": ejercicioEntrenado[1].nombre,
                "fecha": ejercicioEntrenado[0].fecha,
                "fechaDate": datetime.datetime.strptime(ejercicioEntrenado[0].fecha, "%Y-%m-%d"),
                "repeticiones": ejercicioEntrenado[0].repeticiones,
                "tiempo": ejercicioEntrenado[0].tiempo,
            }

    def dar_entrenamientos(self, id_persona):
        persona = self.dar_persona(id_persona)
        ejerciciosEntrenado = (self.dar_ejercicio_entrenados_por_persona_id(persona["id"]))
        result = []
        for ejercicioEntrenado in ejerciciosEntrenado:
            result.append(self.mapear_objeto_entrenamiento(ejercicioEntrenado))

        return sorted(
            result,
            key=lambda entrenamiento: (entrenamiento["fechaDate"], entrenamiento["ejercicio"]),
            reverse=True,
        )

    def validar_crear_editar_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        error = ""
        str_to_date = datetime.datetime.now()
        repeticiones_to_int = 0

        if self.es_diccionario_vacio(persona):
            error = "Error, el diccionario persona esta vacio"

        if not error and len(ejercicio) == 0:
            error = "Error, el campo ejercicio esta vacio"

        if not error and len(fecha) == 0:
            error = "Error, el campo fecha esta vacio"

        if not error:
            try:
                formato_dia = '%Y-%m-%d'
                str_to_date = self.obtener_fecha_de_string(fecha, formato_dia)
            except ValueError:
                error = "Error, la fecha no es valida. Debe tener formato YYYY-MM-DD"

        if not error and (not self.fecha_menor_igual_dia_actual(str_to_date)):
            error = "Error, la fecha ingresada debe ser igual o menor al dia de hoy"

        if not error:
            try:
                repeticiones_to_int = int(repeticiones)
            except ValueError:
                error = "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero"

        if not error and repeticiones_to_int < 0:
            error = "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero"

        if not error and len(tiempo) == 0:
            error = "Error, el tiempo esta vacio"

        if not error and not self.tiempo_tiene_formato_valido(tiempo):
            error = "Error, el tiempo no es valida. Debe tener formato hh:mm:ss"

        return error

    def crear_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        objeto_ejercicio = self.dar_ejercicio_por_nombre(ejercicio)

        entrenamiento = EjercicioEntrenado(persona_id=persona["id"], ejercicio_id=objeto_ejercicio.id, fecha=fecha,
                              repeticiones=repeticiones, tiempo=tiempo)
        session.add(entrenamiento)
        session.commit()

        return True

    def dar_historial_ejercicios_entrenados_por_persona_id(self, persona_id):
        return ((session.query(
            EjercicioEntrenado,
            func.sum(EjercicioEntrenado.repeticiones),
            func.sum(EjercicioEntrenado.repeticiones * Ejercicio.calorias),
        ).join(Ejercicio, EjercicioEntrenado.ejercicio_id == Ejercicio.id)
                .filter(EjercicioEntrenado.persona_id == persona_id))
                .group_by("fecha").order_by(desc("fecha")).all())

    def dar_reporte(self, id_persona):
        entrenamientos_data = []
        persona = self.dar_persona(id_persona)
        total_repeticiones = 0
        total_calorias = 0

        historial_ejercicios_entrenados = (self.dar_historial_ejercicios_entrenados_por_persona_id(persona["id"]))

        for item in historial_ejercicios_entrenados:
            entrenamientos_data.append({
                "fecha": item[0].fecha,
                "repeticiones": item[1],
                "calorias": item[2],
            })

            total_repeticiones += item[1]
            total_calorias += item[2]

        imc = self.calcular_imc(persona["peso"], persona["talla"])
        clasificacion = self.calcular_clasificacion_imc(imc)

        return {
            "persona": persona,
            "estadisticas": {
                "total_repeticiones": total_repeticiones,
                "total_calorias": total_calorias,
                "imc": imc,
                "clasificacion": clasificacion,
                "entrenamientos": entrenamientos_data
            }
        }