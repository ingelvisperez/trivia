# app/models/trivia.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Trivia(Base):
    __tablename__ = "trivias"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String, nullable=True)

    # relaciones many-to-many con preguntas y usuarios
    questions = relationship("TriviaQuestion", back_populates="trivia")
    assignments = relationship("TriviaAssignment", back_populates="trivia")
    participations = relationship("Participation", back_populates="trivia")
