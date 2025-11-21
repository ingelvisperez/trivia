# app/models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)

    # Relación con asignaciones y participaciones
    assignments = relationship("TriviaAssignment", back_populates="user")
    participations = relationship("Participation", back_populates="user")
