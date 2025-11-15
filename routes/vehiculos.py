from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehiculo
from schemas import VehiculoCreate, Vehiculo as VehiculoSchema

router = APIRouter()

@router.post("/", response_model=VehiculoSchema)
def crear_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo = Vehiculo(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/", response_model=list[VehiculoSchema])
def listar_vehiculos(db: Session = Depends(get_db)):
    return db.query(Vehiculo).filter(Vehiculo.activo == True).all()


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