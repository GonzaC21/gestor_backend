from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_ingreso = Column(String)
    marca = Column(String)
    modelo = Column(String)
    dominio = Column(String)
    chasis = Column(String)
    motor = Column(String)
    color = Column(String)
    estado_general = Column(String)
    estado = Column(String)
    llave = Column(String)
    sumario = Column(String)
    causa = Column(String)
    magistrado = Column(String)
    dependencia = Column(String)
    ubicacion = Column(String)
    activo = Column(Boolean, default=True)