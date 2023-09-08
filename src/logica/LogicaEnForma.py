from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import session

import validators

from src.modelo.ejercicio import Ejercicio


class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        ""

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        if len(nombre) == 0:
            return "Error, el campo nombre esta vacio"

        if len(nombre) >40:
            return "Error, el campo nombre supera los 40 caracteres"

        if len(descripcion) == 0:
            return "Error, el campo descripcion esta vacio"

        if len(descripcion) >250:
            return "Error, el campo descripcion supera los 250 caracteres"

        if len(enlace) == 0:
            return "Error, el campo enlace esta vacio"

        if len(enlace) == 0:
            return "Error, el campo enlace esta vacio"

        if not validators.url(enlace):
            return "Error, el campo enlace es incorrecto"

        if "https://www.youtube.com/" not in enlace:
            return "Error, el campo enlace no es de Youtube"

        if type(calorias) != int:
            return "Error, el campo calorias debe ser un número entero"

        if calorias <= 0:
            return "Error, el campo calorias debe ser mayor a cero"

        busqueda = session.query(Ejercicio).filter(Ejercicio.nombre == nombre).all()

        if len(busqueda) > 0:
            return "Error, el ejericio "+nombre+" ya existe"

        return ""