from sqlalchemy import asc

from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import session

import validators

from src.modelo.ejercicio import Ejercicio
from src.modelo.persona import Persona

class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        ""

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        error = ""

        if len(nombre) == 0:
            error = "Error, el campo nombre esta vacio"

        elif len(nombre) > 40:
            error = "Error, el campo nombre supera los 40 caracteres"

        elif len(descripcion) == 0:
            error = "Error, el campo descripcion esta vacio"

        elif len(descripcion) > 250:
            error = "Error, el campo descripcion supera los 250 caracteres"

        elif len(enlace) == 0:
            error = "Error, el campo enlace esta vacio"

        elif not validators.url(enlace):
            error = "Error, el campo enlace es incorrecto"

        elif "https://www.youtube.com/" not in enlace:
            error = "Error, el campo enlace no es de Youtube"

        #elif type(calorias) != int:
         #   error = "Error, el campo calorias debe ser un número entero"

        elif int(calorias) <= 0:
            error = "Error, el campo calorias debe ser mayor a cero"

        else:
            busqueda = session.query(Ejercicio).filter(Ejercicio.nombre == nombre).all()

            if len(busqueda) > 0:
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
