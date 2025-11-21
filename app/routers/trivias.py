# app/routers/trivias.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trivia import Trivia
from app.models.trivia_question import TriviaQuestion
from app.models.trivia_assignment import TriviaAssignment
from app.models.question import Question
from app.models.user import User
from app.models.participation import Participation

from app.schemas.trivia import (
    TriviaCreate,
    TriviaRead,
    TriviaDetail,
    TriviaPlay,
    TriviaPlayQuestion,
    TriviaAnswerIn,
    TriviaAnswerResult,
)
from app.schemas.question import QuestionRead
from app.services.scoring_service import calculate_score

router = APIRouter()


# ---------- CRUD básico de trivias ----------

@router.post("/", response_model=TriviaRead, status_code=status.HTTP_201_CREATED)
def create_trivia(trivia_in: TriviaCreate, db: Session = Depends(get_db)):
    # Validar preguntas existentes
    if not trivia_in.question_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La trivia debe tener al menos una pregunta.",
        )

    questions = (
        db.query(Question)
        .filter(Question.id.in_(trivia_in.question_ids))
        .all()
    )
    if len(questions) != len(trivia_in.question_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Una o más preguntas no existen.",
        )

    # Validar usuarios (si se enviaron)
    users = []
    if trivia_in.user_ids:
        users = (
            db.query(User)
            .filter(User.id.in_(trivia_in.user_ids))
            .all()
        )
        if len(users) != len(trivia_in.user_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno o más usuarios no existen.",
            )

    # Crear la trivia
    trivia = Trivia(
        name=trivia_in.name,
        description=trivia_in.description,
    )
    db.add(trivia)
    db.flush()  # obtenemos trivia.id sin hacer commit aún

    # Asociar preguntas a la trivia
    for order, q_id in enumerate(trivia_in.question_ids):
        tq = TriviaQuestion(
            trivia_id=trivia.id,
            question_id=q_id,
            order=order,
        )
        db.add(tq)

    # Asignar usuarios a la trivia
    if trivia_in.user_ids:
        for user_id in trivia_in.user_ids:
            assign = TriviaAssignment(
                trivia_id=trivia.id,
                user_id=user_id,
            )
            db.add(assign)

    db.commit()
    db.refresh(trivia)

    return trivia


@router.get("/", response_model=List[TriviaRead])
def list_trivias(db: Session = Depends(get_db)):
    trivias = db.query(Trivia).all()
    return trivias


@router.get("/{trivia_id}", response_model=TriviaDetail)
def get_trivia(trivia_id: int, db: Session = Depends(get_db)):
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia no encontrada.",
        )

    # Obtener preguntas asociadas
    questions = (
        db.query(Question)
        .join(TriviaQuestion, TriviaQuestion.question_id == Question.id)
        .filter(TriviaQuestion.trivia_id == trivia_id)
        .order_by(TriviaQuestion.order)
        .all()
    )

    return TriviaDetail(
        id=trivia.id,
        name=trivia.name,
        description=trivia.description,
        questions=questions,  # Pydantic lo convertirá a QuestionRead gracias a orm_mode
    )


# ---------- Jugar una trivia ----------

@router.get("/{trivia_id}/play", response_model=TriviaPlay)
def play_trivia(trivia_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la trivia asignada a un usuario, ocultando la respuesta correcta y la dificultad.
    """
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia no encontrada.",
        )

    # Verificar que el usuario tenga esta trivia asignada
    assignment = (
        db.query(TriviaAssignment)
        .filter(
            TriviaAssignment.trivia_id == trivia_id,
            TriviaAssignment.user_id == user_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene asignada esta trivia.",
        )

    # Obtener preguntas asociadas
    questions = (
        db.query(Question)
        .join(TriviaQuestion, TriviaQuestion.question_id == Question.id)
        .filter(TriviaQuestion.trivia_id == trivia_id)
        .order_by(TriviaQuestion.order)
        .all()
    )

    play_questions = [
        TriviaPlayQuestion(
            id=q.id,
            text=q.text,
            options=q.options,
        )
        for q in questions
    ]

    return TriviaPlay(
        trivia_id=trivia.id,
        name=trivia.name,
        description=trivia.description,
        questions=play_questions,
    )


# ---------- Responder una trivia ----------

@router.post("/{trivia_id}/answer", response_model=TriviaAnswerResult)
def answer_trivia(
    trivia_id: int,
    payload: TriviaAnswerIn,
    db: Session = Depends(get_db),
):
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia no encontrada.",
        )

    # Verificar que el usuario tenga esta trivia asignada
    assignment = (
        db.query(TriviaAssignment)
        .filter(
            TriviaAssignment.trivia_id == trivia_id,
            TriviaAssignment.user_id == payload.user_id,
        )
        .first()
    )
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene asignada esta trivia.",
        )

    # Obtener preguntas de la trivia
    questions = (
        db.query(Question)
        .join(TriviaQuestion, TriviaQuestion.question_id == Question.id)
        .filter(TriviaQuestion.trivia_id == trivia_id)
        .order_by(TriviaQuestion.order)
        .all()
    )

    # Calcular puntaje
    score, max_score, correct, wrong = calculate_score(questions, payload.answers)

    # Registrar participación
    participation = Participation(
        user_id=payload.user_id,
        trivia_id=trivia_id,
        answers=payload.answers,
        score=score,
    )
    db.add(participation)
    db.commit()

    return TriviaAnswerResult(
        trivia_id=trivia_id,
        user_id=payload.user_id,
        score=score,
        max_score=max_score,
        correct_answers=correct,
        wrong_answers=wrong,
    )
