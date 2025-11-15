from pydantic import BaseModel

class VehiculoBase(BaseModel):
    fecha_ingreso: str
    marca: str
    modelo: str
    dominio: str
    chasis: str
    motor: str
    color: str
    estado_general: str
    estado: str
    llave: str
    sumario: str
    causa: str
    magistrado: str
    dependencia: str
    ubicacion: str
    activo: bool = True

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id: int

    class Config:
        from_attributes = True