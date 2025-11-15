from fastapi import FastAPI
from database import Base, engine        # <- SOLO importamos desde database.py
from routes import vehiculos

# Crear tablas automáticamente en PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Registrar rutas
app.include_router(vehiculos.router, prefix="/vehiculos", tags=["Vehículos"])

@app.get("/")
def root():
    return {"status": "API funcionando con PostgreSQL 🚀"}
