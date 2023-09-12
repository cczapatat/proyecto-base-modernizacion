import datetime
import enum

from sqlalchemy import asc

from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import session

import validators
import re

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
        ""

    def mapper_none_to_empty(self, value):
        temporal_value = value

        if value is None:
            temporal_value = ""

        return temporal_value

    def es_diccionario_vacio(self, dict):
        return bool(dict) is False

    def obtener_fecha_de_string(self, str_fecha, formato):
        return datetime.datetime.strptime(str_fecha, formato)

    def fecha_menor_igual_dia_actual(self, fecha):
        return fecha <= datetime.datetime.now()

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
        has_error = False
        calorias_int = 0

        if not has_error and len(nombre) == 0:
            has_error = True
            error = "Error, el campo nombre esta vacio"

        if not has_error and len(nombre) > 40:
            has_error = True
            error = "Error, el campo nombre supera los 40 caracteres"

        if not has_error and len(descripcion) == 0:
            has_error = True
            error = "Error, el campo descripcion esta vacio"

        if not has_error and len(descripcion) > 250:
            has_error = True
            error = "Error, el campo descripcion supera los 250 caracteres"

        if not has_error and len(enlace) == 0:
            has_error = True
            error = "Error, el campo enlace esta vacio"

        if not has_error and (not validators.url(enlace)):
            has_error = True
            error = "Error, el campo enlace es incorrecto"

        if not has_error and "https://www.youtube.com/" not in enlace:
            has_error = True
            error = "Error, el campo enlace no es de Youtube"

        if not has_error:
            try:
                calorias_int = int(calorias)
            except ValueError:
                has_error = True
                error = "Error, el campo calorias debe ser un número entero"

        if not has_error and calorias_int <= 0:
            has_error = True
            error = "Error, el campo calorias debe ser mayor a cero"

        busqueda = session.query(Ejercicio).filter(Ejercicio.nombre == nombre).all()

        if not has_error and len(busqueda) > 0:
            error = "Error, el ejericio " + nombre + " ya existe"

        return error

    def crear_ejercicio(self, nombre, descripcion, enlace, calorias):
        ejercicio = Ejercicio(nombre=nombre, descripcion=descripcion, youtube=enlace,
                              calorias=calorias)
        session.add(ejercicio)
        session.commit()

        return True

    def dar_ejercici_por_nombre (self, nombre_ejercicio):
        return session.query(Ejercicio).filter(Ejercicio.nombre == nombre_ejercicio).first()


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
            persona_dict["fecha_retiro"] = self.mapper_none_to_empty(persona_dict["fecha_retiro"])
            persona_dict["razon_retiro"] = self.mapper_none_to_empty(persona_dict["razon_retiro"])

            result.append(persona_dict)

        return result

    def dar_persona(self, id_persona):
        personas = self.dar_personas()

        return personas[id_persona]

    def dar_entrenamientos(self, id_persona):
        persona = self.dar_persona(id_persona)
        ejerciciosEntrenado = (session.query(EjercicioEntrenado, Ejercicio)
                               .join(Ejercicio, EjercicioEntrenado.ejercicio_id == Ejercicio.id)
                               .filter(EjercicioEntrenado.persona_id == persona["id"]).all())
        result = []
        for ejercicioEntrenado in ejerciciosEntrenado:
            result.append({
                "id": ejercicioEntrenado[0].id,
                "ejercicio_id": ejercicioEntrenado[0].ejercicio_id,
                "ejercicio": ejercicioEntrenado[1].nombre,
                "fecha": ejercicioEntrenado[0].fecha,
                "fechaDate": datetime.datetime.strptime(ejercicioEntrenado[0].fecha, "%Y-%m-%d"),
                "repeticiones": ejercicioEntrenado[0].repeticiones,
                "tiempo": ejercicioEntrenado[0].tiempo,
            })

        return sorted(
            result,
            key=lambda entrenamiento: (entrenamiento["fechaDate"], entrenamiento["ejercicio"]),
            reverse=True,
        )

    def validar_crear_editar_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        error = ""
        has_error = False
        str_to_date = datetime.datetime.now()
        repeticiones_to_int = 0

        if self.es_diccionario_vacio(persona):
            has_error = True
            error = "Error, el diccionario persona esta vacio"

        if not has_error and len(ejercicio) == 0:
            has_error = True
            error = "Error, el campo ejercicio esta vacio"

        if not has_error and len(fecha) == 0:
            has_error = True
            error = "Error, el campo fecha esta vacio"

        if not has_error:
            try:
                formato_dia = '%Y-%m-%d'
                str_to_date = self.obtener_fecha_de_string(fecha, formato_dia)
            except ValueError:
                has_error = True
                error = "Error, la fecha no es valida. Debe tener formato YYYY-MM-DD"

        if not has_error and (not self.fecha_menor_igual_dia_actual(str_to_date)):
            has_error = True
            error = "Error, la fecha ingresada debe ser igual o menor al dia de hoy"

        if not has_error:
            try:
                repeticiones_to_int = int(repeticiones)
            except ValueError:
                has_error = True
                error = "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero"

        if not has_error and repeticiones_to_int < 0:
            has_error = True
            error = "Error, la cantidad de repeticiones debe ser un numero entero mayor a cero"

        if not has_error and len(tiempo) == 0:
            has_error = True
            error = "Error, el tiempo esta vacio"

        if not has_error and not re.findall("\d\d:\d\d:\d\d", tiempo):
            error = "Error, el tiempo no es valida. Debe tener formato hh:mm:ss"

        return error

    def crear_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        objeto_ejercicio = self.dar_ejercici_por_nombre(ejercicio)

        entrenamiento = EjercicioEntrenado(persona_id=persona["id"], ejercicio_id=objeto_ejercicio.id, fecha=fecha,
                              repeticiones=repeticiones, tiempo=tiempo)
        session.add(entrenamiento)
        session.commit()

        return True

    def dar_reporte(self, id_persona):
        persona = self.dar_persona(id_persona)
        imc = self.calcular_imc(persona["peso"], persona["talla"])
        clasificacion = self.calcular_clasificacion_imc(imc)

        return {
            "persona": persona,
            "estadisticas": {
                "total_repeticiones": 0,
                "total_calorias": 0,
                "imc": imc,
                "clasificacion": clasificacion,
                "entrenamientos": []
            }
        }