from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
from db import init_db
from routes import vehiculos

# ============================================================
# 🚀 CONFIGURACIÓN PRINCIPAL DE LA API
# ============================================================

app = FastAPI(title="Gestor Vehículos API", version="1.0")

# --- Permitir acceso desde cualquier origen (para frontend/desktop app) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Podés limitar esto si querés más seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registrar las rutas principales ---
app.include_router(vehiculos.router, prefix="/vehiculos", tags=["Vehículos"])

# --- Inicializar base de datos al arrancar ---
@app.on_event("startup")
def startup():
    init_db()

# --- Endpoint raíz de prueba ---
@app.get("/")
def root():
    return {"message": "🚗 API del Gestor de Vehículos funcionando correctamente"}


# ============================================================
# 🚘 ENDPOINT ADICIONAL: EGRESAR VEHÍCULO (dar de baja)
# ============================================================

class EgresoRequest(BaseModel):
    tipo: Optional[str] = "entregado"
    motivo: Optional[str] = None


@app.put("/vehiculos/{vehiculo_id}/egreso")
def egresar_vehiculo(vehiculo_id: int, data: EgresoRequest):
    """
    Marca un vehículo como egresado (dado de baja) en la base de datos SQLite.
    """
    try:
        conn = sqlite3.connect("vehiculos.db")
        c = conn.cursor()

        # Verificar existencia
        c.execute("SELECT id FROM vehiculos WHERE id = ?", (vehiculo_id,))
        row = c.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        # Actualizar el registro
        c.execute("""
            UPDATE vehiculos
            SET activo = 0,
                estado_general = ?,
                ubicacion = COALESCE(?, ubicacion)
            WHERE id = ?
        """, (f"Baja: {data.tipo or 'entregado'}", data.motivo, vehiculo_id))

        conn.commit()
        return {"mensaje": f"✅ Vehículo {vehiculo_id} egresado correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al dar de baja el vehículo: {e}")
    
    finally:
        conn.close()
