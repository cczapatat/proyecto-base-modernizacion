from src.logica.FachadaEnForma import FachadaEnForma


class LogicaEnForma(FachadaEnForma):

    def __init__(self):
        ""

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        if len(nombre) == 0:
            return "Error, el campo nombre esta vacio"

        return ""