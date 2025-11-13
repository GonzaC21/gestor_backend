from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from db import init_db, SessionLocal, Vehiculo
from routes import vehiculos

app = FastAPI(title="Gestor Vehículos API", version="1.0")

# --- Configurar CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registrar routers ---
app.include_router(vehiculos.router, prefix="/vehiculos", tags=["Vehículos"])

# --- Inicialización de la BD al iniciar ---
@app.on_event("startup")
def startup():
    init_db()

# --- Endpoint raíz ---
@app.get("/")
def root():
    return {"message": "🚗 API del Gestor de Vehículos funcionando correctamente"}


# ============================================================
# 🚘 ENDPOINT NUEVO: EGRESAR VEHÍCULO
# ============================================================

class EgresoRequest(BaseModel):
    tipo: Optional[str] = "entregado"
    motivo: Optional[str] = None


@app.put("/vehiculos/{vehiculo_id}/egreso")
def egresar_vehiculo(vehiculo_id: int, data: EgresoRequest):
    """
    Marca un vehículo como egresado (dado de baja) en la base de datos.
    """
    db: Session = SessionLocal()
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id == vehiculo_id).first()

    if not vehiculo:
        db.close()
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    vehiculo.activo = 0
    vehiculo.estado_general = f"Baja: {data.tipo or 'entregado'}"
    if data.motivo:
        vehiculo.ubicacion = data.motivo

    db.commit()
    db.refresh(vehiculo)
    db.close()

    return {"mensaje": f"Vehículo {vehiculo_id} egresado correctamente"}
