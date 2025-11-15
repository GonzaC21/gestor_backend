from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehiculo
from schemas import VehiculoCreate, Vehiculo as VehiculoSchema

router = APIRouter()

# ============================================================
#  CREAR VEHÍCULO
# ============================================================
@router.post("/", response_model=VehiculoSchema)
def crear_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    nuevo = Vehiculo(**data.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ============================================================
#  LISTAR VEHÍCULOS (SOLO ACTIVOS)
# ============================================================
@router.get("/", response_model=list[VehiculoSchema])
def listar_vehiculos(
    fecha_ingreso: str | None = None,
    marca: str | None = None,
    modelo: str | None = None,
    dominio: str | None = None,
    chasis: str | None = None,
    motor: str | None = None,
    activos_only: bool = True,
    db: Session = Depends(get_db)
):

    query = db.query(Vehiculo)

    if activos_only:
        query = query.filter(Vehiculo.activo == True)

    if fecha_ingreso:
        query = query.filter(Vehiculo.fecha_ingreso == fecha_ingreso)
    if marca:
        query = query.filter(Vehiculo.marca.ilike(f"%{marca}%"))
    if modelo:
        query = query.filter(Vehiculo.modelo.ilike(f"%{modelo}%"))
    if dominio:
        query = query.filter(Vehiculo.dominio.ilike(f"%{dominio}%"))
    if chasis:
        query = query.filter(Vehiculo.chasis.ilike(f"%{chasis}%"))
    if motor:
        query = query.filter(Vehiculo.motor.ilike(f"%{motor}%"))

    return query.all()


# ============================================================
#  OBTENER VEHÍCULO POR ID
# ============================================================
@router.get("/{vehiculo_id}", response_model=VehiculoSchema)
def obtener_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return veh


# ============================================================
#  DAR DE BAJA (DESACTIVAR)
# ============================================================
@router.put("/{vehiculo_id}/baja")
def baja_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    veh.activo = False
    db.commit()
    return {"mensaje": "Vehículo dado de baja"}


# ============================================================
#  NUEVA RUTA DE EGRESO (TOMA TIPO + MOTIVO)
# ============================================================
@router.put("/{vehiculo_id}/egreso")
def egreso_vehiculo(
    vehiculo_id: int,
    data: dict,
    db: Session = Depends(get_db)
):
    veh = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    tipo = data.get("tipo")
    motivo = data.get("motivo")

    # Marca el vehículo como inactivo
    veh.activo = False

    # Guarda los datos del egreso
    if tipo:
        veh.estado_general = tipo
    if motivo:
        veh.causa = motivo

    db.commit()
    db.refresh(veh)

    return {"mensaje": "Vehículo egresado correctamente", "vehiculo_id": vehiculo_id}
