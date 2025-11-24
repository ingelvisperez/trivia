# app/routers/ranking.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trivia import Trivia
from app.models.participation import Participation
from app.models.user import User
from app.schemas.ranking import RankingEntry

router = APIRouter()


@router.get("/{trivia_id}", response_model=List[RankingEntry])
def get_ranking(trivia_id: int, db: Session = Depends(get_db)):
    """
    Devuelve el ranking de usuarios para una trivia específica,
    ordenado por puntaje de mayor a menor.
    """
    # Validación que la trivia exista
    trivia = db.query(Trivia).filter(Trivia.id == trivia_id).first()
    if not trivia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia no encontrada.",
        )

    # Obtener participaciones con join a User
    rows = (
        db.query(Participation, User)
        .join(User, Participation.user_id == User.id)
        .filter(Participation.trivia_id == trivia_id)
        .order_by(Participation.score.desc(), Participation.created_at.asc())
        .all()
    )

    ranking: List[RankingEntry] = []
    for idx, (p, u) in enumerate(rows, start=1):
        ranking.append(
            RankingEntry(
                position=idx,
                user_id=u.id,
                user_name=u.name,
                score=p.score,
                created_at=p.created_at
                
            )
        )

    return ranking
