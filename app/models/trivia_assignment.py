# app/models/trivia_assignment.py
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TriviaAssignment(Base):
    __tablename__ = "trivia_assignments"

    id = Column(Integer, primary_key=True, index=True)
    trivia_id = Column(Integer, ForeignKey("trivias.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    trivia = relationship("Trivia", back_populates="assignments")
    user = relationship("User", back_populates="assignments")
