from sqlalchemy import Column, Integer, String, ForeignKey

from .declarative_base import Base

class EjercicioEntrenado(Base):
    __tablename__ = 'ejercicios_entrenados'

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey('personas.id'))
    ejercicio_id = Column(Integer, ForeignKey('ejercicios.id'))
    fecha = Column(String)
    repeticiones = Column(Integer)
    tiempo = Column(String)