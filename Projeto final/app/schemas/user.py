from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# --- Request Schemas ---

class UserCreate(BaseModel):
    """Schema para registro de novo usuário."""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema para login."""
    username: str
    password: str


# --- Response Schemas ---

class UserResponse(BaseModel):
    """Schema de resposta com dados do usuário (sem senha)."""
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Schema de resposta do token JWT."""
    access_token: str
    token_type: str = "bearer"
