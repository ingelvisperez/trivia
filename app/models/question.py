# app/models/question.py
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class DifficultyEnum(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    # dificultad: easy | medium | hard
    difficulty = Column(Enum(DifficultyEnum), nullable=False)

    # opciones: array / lista de strings (guardado como JSONB en Postgres)
    options = Column(JSONB, nullable=False)

    # podemos guardar el índice de la opción correcta o el texto
    correct_option = Column(String, nullable=False)

    trivias = relationship("TriviaQuestion", back_populates="question")
