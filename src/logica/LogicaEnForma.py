from src.logica.FachadaEnForma import FachadaEnForma


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

        return ""