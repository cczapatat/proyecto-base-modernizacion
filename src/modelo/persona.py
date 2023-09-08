from sqlalchemy import Column, Integer, String, Date, REAL

from .declarative_base import Base

class Persona(Base):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)
    fechaInicio = Column(Date)
    fechaFin = Column(Date)
    razonFin = Column(String)
    talla = Column(REAL)
    peso = Column(REAL)
    edad = Column(Integer)
    medidaBrazo = Column(Integer)
    medidaPierna = Column(Integer)
    medidaPecho = Column(Integer)
    medidaCintura = Column(Integer)