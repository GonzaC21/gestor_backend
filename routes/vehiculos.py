from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehiculo
from schemas import VehiculoCreate, Vehiculo as VehiculoSchema
from typing import Optional

router = APIRouter()

@router.post("/", response_model=VehiculoSchema)
def crear_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo = Vehiculo(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[VehiculoSchema])
def listar_vehiculos(
    fecha_ingreso: Optional[str] = None,
    marca: Optional[str] = None,
    modelo: Optional[str] = None,
    dominio: Optional[str] = None,
    chasis: Optional[str] = None,
    motor: Optional[str] = None,
    activos_only: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(Vehiculo)

    # --- Filtros dinámicos ---
    if fecha_ingreso:
        query = query.filter(Vehiculo.fecha_ingreso.contains(fecha_ingreso))

    if marca:
        query = query.filter(Vehiculo.marca.contains(marca))

    if modelo:
        query = query.filter(Vehiculo.modelo.contains(modelo))

    if dominio:
        query = query.filter(Vehiculo.dominio.contains(dominio))

    if chasis:
        query = query.filter(Vehiculo.chasis.contains(chasis))

    if motor:
        query = query.filter(Vehiculo.motor.contains(motor))

    # Mostrar solo activos
    if activos_only:
        query = query.filter(Vehiculo.activo == True)

    return query.all()


@router.get("/{vehiculo_id}", response_model=VehiculoSchema)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return veh


@router.put("/{vehiculo_id}/baja")
def baja_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    veh.activo = False
    db.commit()
    return {"mensaje": "Vehículo dado de baja"}
