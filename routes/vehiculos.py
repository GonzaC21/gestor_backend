from fastapi import APIRouter, HTTPException
from db import get_connection
from models import Vehiculo, VehiculoCreate

router = APIRouter()

@router.post("/", response_model=Vehiculo)
def crear_vehiculo(data: VehiculoCreate):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO vehiculos 
        (fecha_ingreso, marca, modelo, dominio, chasis, motor, color, estado_general, estado, llave, sumario, causa, magistrado, dependencia, ubicacion, activo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.fecha_ingreso, data.marca, data.modelo, data.dominio, data.chasis,
        data.motor, data.color, data.estado_general, data.estado, data.llave,
        data.sumario, data.causa, data.magistrado, data.dependencia, data.ubicacion, data.activo
    ))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return {**data.dict(), "id": new_id}

@router.get("/", response_model=list[Vehiculo])
def listar_vehiculos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM vehiculos WHERE activo = 1")
    rows = c.fetchall()
    conn.close()

    columnas = [desc[0] for desc in c.description]
    return [dict(zip(columnas, row)) for row in rows]

@router.get("/{vehiculo_id}", response_model=Vehiculo)
def obtener_vehiculo(vehiculo_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM vehiculos WHERE id = ?", (vehiculo_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    columnas = [desc[0] for desc in c.description]
    return dict(zip(columnas, row))

@router.delete("/{vehiculo_id}")
def eliminar_vehiculo(vehiculo_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE vehiculos SET activo = 0 WHERE id = ?", (vehiculo_id,))
    conn.commit()
    conn.close()
    return {"message": f"Vehículo {vehiculo_id} marcado como inactivo."}
