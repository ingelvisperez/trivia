# app/schemas/user.py
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Esquema para crear usuario (request)."""
    pass


class UserRead(UserBase):
    """Esquema para devolver usuario (response)."""
    id: int

    class Config:
        orm_mode = True  # permite convertir desde objetos SQLAlchemy
