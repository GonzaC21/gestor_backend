from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehiculo
from schemas import VehiculoCreate, Vehiculo as VehiculoSchema

router = APIRouter()

# =====================================================
#   CREAR VEHÍCULO
# =====================================================
@router.post("/", response_model=VehiculoSchema)
def crear_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo = Vehiculo(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# =====================================================
#   LISTAR VEHÍCULOS (ACTIVOS, INACTIVOS, FILTROS)
# =====================================================
@router.get("/", response_model=list[VehiculoSchema])
def listar_vehiculos(
    db: Session = Depends(get_db),
    marca: str = None,
    dominio: str = None,
    motor: str = None,
    activos_only: int = 1   # 1 = solo activos | 0 = todos
):
    query = db.query(Vehiculo)

    # ---- Filtro de activos / inactivos ----
    if activos_only == 1:
        query = query.filter(Vehiculo.activo == True)

    # ---- Filtros opcionales ----
    if marca:
        query = query.filter(Vehiculo.marca.ilike(f"%{marca}%"))

    if dominio:
        query = query.filter(Vehiculo.dominio.ilike(f"%{dominio}%"))

    if motor:
        query = query.filter(Vehiculo.motor.ilike(f"%{motor}%"))

    return query.all()


# =====================================================
#   OBTENER VEHÍCULO POR ID
# =====================================================
@router.get("/{vehiculo_id}", response_model=VehiculoSchema)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return veh


# =====================================================
#   BAJA (EGRESO) VEHÍCULO
# =====================================================
@router.put("/{vehiculo_id}/baja")
def baja_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    veh.activo = False
    db.commit()

    return {"mensaje": "Vehículo dado de baja correctamente"}
