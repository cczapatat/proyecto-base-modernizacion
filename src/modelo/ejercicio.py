from sqlalchemy import Column, Integer, String

from .declarative_base import Base

class Ejercicio(Base):
    __tablename__ = 'ejercicios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    calorias = Column(Integer)
    youtube = Column(String)