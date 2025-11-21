# app/schemas/question.py
from typing import List
from pydantic import BaseModel, ConfigDict
from app.models.question import DifficultyEnum


class QuestionBase(BaseModel):
    text: str
    difficulty: DifficultyEnum
    options: List[str]
    correct_option: str  # texto o índice, pero consistente


class QuestionCreate(QuestionBase):
    """Esquema para crear preguntas (request)."""
    pass


class QuestionRead(QuestionBase):
    """Esquema para devolver preguntas (response)."""
    id: int

    # Pydantic v2 -> equivalente moderno de orm_mode = True
    model_config = ConfigDict(from_attributes=True)
