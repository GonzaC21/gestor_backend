from fastapi import FastAPI
from database import Base, engine
from routes import vehiculos
from db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vehiculos.router, prefix="/vehiculos", tags=["Vehículos"])

@app.get("/")
def root():
    return {"status": "API funcionando con PostgreSQL 🚀"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)