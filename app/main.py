# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import user, question, trivia, trivia_question, trivia_assignment, participation

# Cuando arrancas en desarrollo, puedes crear las tablas automáticamente.
# En un entorno productivo lo ideal es usar Alembic para migraciones.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TalaTrivia API",
    description="API para gestionar usuarios, preguntas, trivias y ranking de TalaTrivia.",
    version="1.0.0",
)

# Configuración básica de CORS (puedes ajustarla según tu necesidad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ====== RUTAS BÁSICAS / HEALTHCHECK ======
@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Bienvenido a TalaTrivia API"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


# ====== INCLUSIÓN DE ROUTERS ======
from app.routers import users, questions, trivias, ranking

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(trivias.router, prefix="/trivias", tags=["Trivias"])
app.include_router(ranking.router, prefix="/ranking", tags=["Ranking"])
