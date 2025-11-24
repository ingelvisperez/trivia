# app/models/trivia_question.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TriviaQuestion(Base):
    __tablename__ = "trivia_questions"

    id = Column(Integer, primary_key=True, index=True)
    trivia_id = Column(Integer, ForeignKey("trivias.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    # Para mantener el orden de las preguntas
    order = Column(Integer, nullable=True)

    trivia = relationship("Trivia", back_populates="questions")
    question = relationship("Question", back_populates="trivias")
