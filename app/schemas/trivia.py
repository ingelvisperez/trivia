# app/schemas/trivia.py
from typing import List, Dict, Optional
from pydantic import BaseModel

from app.schemas.question import QuestionRead


# ---------- Esquemas básicos de Trivia ----------

class TriviaBase(BaseModel):
    name: str
    description: Optional[str] = None


class TriviaCreate(TriviaBase):
    question_ids: List[int]
    user_ids: Optional[List[int]] = None


class TriviaRead(TriviaBase):
    id: int

    class Config:
        orm_mode = True


class TriviaDetail(TriviaRead):
    questions: List[QuestionRead]


# ---------- Esquemas para jugar la trivia ----------

class TriviaPlayQuestion(BaseModel):
    id: int
    text: str
    options: List[str]


class TriviaPlay(BaseModel):
    trivia_id: int
    name: str
    description: Optional[str] = None
    questions: List[TriviaPlayQuestion]


# ---------- Esquemas para responder la trivia ----------

class TriviaAnswerIn(BaseModel):
    user_id: int
    # answers: question_id -> opción elegida (texto)
    answers: Dict[int, str]


class TriviaAnswerResult(BaseModel):
    trivia_id: int
    user_id: int
    score: int
    max_score: int
    correct_answers: int
    wrong_answers: int
