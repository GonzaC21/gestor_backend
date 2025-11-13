from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
from db import init_db
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

# --- Inicializar BD ---
@app.on_event("startup")
def startup():
    init_db()

# --- Endpoint raíz ---
@app.get("/")
def root():
    return {"message": "🚗 API del Gestor de Vehículos funcionando correctamente"}


# ============================================================
# 🚘 ENDPOINT NUEVO: EGRESAR VEHÍCULO (dar de baja)
# ============================================================

class EgresoRequest(BaseModel):
    tipo: Optional[str] = "entregado"
    motivo: Optional[str] = None


@app.put("/vehiculos/{vehiculo_id}/egreso")
def egresar_vehiculo(vehiculo_id: int, data: EgresoRequest):
    """
    Marca un vehículo como egresado (dado de baja) en la base de datos SQLite.
    """
    conn = sqlite3.connect("vehiculos.db")
    c = conn.cursor()

    # Buscar el vehículo
    c.execute("SELECT * FROM vehiculos WHERE id = ?", (vehiculo_id,))
    vehiculo = c.fetchone()
    if not vehiculo:
        conn.close()
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Actualizar estado a inactivo (egresado)
    c.execute("""
        UPDATE vehiculos
        SET activo = 0,
            estado_general = ?,
            ubicacion = COALESCE(?, ubicacion)
        WHERE id = ?
    """, (f"Baja: {data.tipo or 'entregado'}", data.motivo, vehiculo_id))

    conn.commit()
    conn.close()

    return {"mensaje": f"Vehículo {vehiculo_id} egresado correctamente"}
