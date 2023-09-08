from src.logica.FachadaEnForma import FachadaEnForma

import validators

class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        ""

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        if len(nombre) == 0:
            return "Error, el campo nombre esta vacio"

        if len(descripcion) == 0:
            return "Error, el campo descripcion esta vacio"

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

        return ""