import datetime

from sqlalchemy import asc

from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import session

import validators

from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona
from src.modelo.ejercicioEntrenado import EjercicioEntrenado


class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        ""

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
            result.append(persona.__dict__)

        return result

    def dar_entrenamientos(self, id_persona):
        ejerciciosEntrenado = (session.query(EjercicioEntrenado, Ejercicio)
                               .join(Ejercicio, EjercicioEntrenado.ejercicio_id == Ejercicio.id)
                               .filter(EjercicioEntrenado.persona_id == id_persona).all())
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
