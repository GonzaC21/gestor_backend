import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render pasa DATABASE_URL con formato postgres://
# SQLAlchemy requiere postgresql://
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Crear el engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de los modelos
Base = declarative_base()


# Dependencia para usar la BD en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
