# app/models/participation.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.database import Base


class Participation(Base):
    __tablename__ = "participations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    trivia_id = Column(Integer, ForeignKey("trivias.id", ondelete="CASCADE"), nullable=False)

    # respuestas del usuario, por ejemplo: {"1": "0", "5": "2"}
    answers = Column(JSONB, nullable=False)

    score = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="participations")
    trivia = relationship("Trivia", back_populates="participations")
