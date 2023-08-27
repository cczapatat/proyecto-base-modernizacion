import sys
from src.vista.InterfazEnForma import App_EnForma
from src.logica.LogicaMock import LogicaMock

if __name__ == '__main__':
    # Punto inicial de la aplicación

    logica = LogicaMock()

    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())