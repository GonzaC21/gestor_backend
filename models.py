from pydantic import BaseModel
from typing import Optional

class VehiculoBase(BaseModel):
    fecha_ingreso: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    dominio: Optional[str] = None
    chasis: Optional[str] = None
    motor: Optional[str] = None
    color: Optional[str] = None
    estado_general: Optional[str] = None
    estado: Optional[str] = None
    llave: Optional[str] = None
    sumario: Optional[str] = None
    causa: Optional[str] = None
    magistrado: Optional[str] = None
    dependencia: Optional[str] = None
    ubicacion: Optional[str] = None
    activo: Optional[int] = 1

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id: int

    class Config:
        from_attributes = True
