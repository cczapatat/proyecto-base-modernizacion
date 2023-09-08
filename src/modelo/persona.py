from sqlalchemy import Column, Integer, String, REAL

from .declarative_base import Base

class Persona(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    fecha_inicio = Column(String)
    fecha_retiro = Column(String)
    razon_retiro = Column(String)
    talla = Column(REAL)
    peso = Column(REAL)
    edad = Column(Integer)
    brazo = Column(Integer)
    pierna = Column(Integer)
    pecho = Column(Integer)
    cintura = Column(Integer)