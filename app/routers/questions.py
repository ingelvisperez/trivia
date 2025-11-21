# app/routers/questions.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionRead

router = APIRouter()


@router.post("/", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(question_in: QuestionCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva pregunta de trivia.
    """
    question = Question(
        text=question_in.text,
        difficulty=question_in.difficulty,
        options=question_in.options,
        correct_option=question_in.correct_option,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get("/", response_model=List[QuestionRead])
def list_questions(db: Session = Depends(get_db)):
    """
    Listar todas las preguntas registradas.
    """
    questions = db.query(Question).all()
    return questions


@router.get("/{question_id}", response_model=QuestionRead)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    Obtener una pregunta por ID.
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregunta no encontrada",
        )
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una pregunta por ID.
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pregunta no encontrada",
        )

    db.delete(question)
    db.commit()
    return
