import sqlite3

DB_NAME = "vehiculos.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Crear tabla de vehículos si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_ingreso TEXT,
            marca TEXT,
            modelo TEXT,
            dominio TEXT,
            chasis TEXT,
            motor TEXT,
            color TEXT,
            estado_general TEXT,
            estado TEXT,
            llave TEXT,
            sumario TEXT,
            causa TEXT,
            magistrado TEXT,
            dependencia TEXT,
            ubicacion TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()
