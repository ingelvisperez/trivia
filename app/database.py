# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ejemplo de DATABASE_URL:
# postgresql://user:password@host:port/dbname
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql://tala:1234@db/talatrivia"  # valor por defecto para docker-compose
# )

DATABASE_URL = "postgresql://tala:1234@localhost:5432/talatrivia"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependencia para usar en FastAPI más adelante
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
