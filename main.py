from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routes import vehiculos

app = FastAPI(title="Gestor Vehículos API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehiculos.router, prefix="/vehiculos", tags=["Vehículos"])

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "🚗 API del Gestor de Vehículos funcionando correctamente"}
