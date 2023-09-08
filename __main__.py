import sys

from src.modelo.declarative_base import Base, engine
from src.vista.InterfazEnForma import App_EnForma
from src.logica.LogicaMock import LogicaMock
from src.logica.LogicaEnForma import LogicaEnForma

if __name__ == '__main__':
    # Punto inicial de la aplicación

    # logica = LogicaMock()

    Base.metadata.create_all(engine)
    logica = LogicaEnForma()

    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())