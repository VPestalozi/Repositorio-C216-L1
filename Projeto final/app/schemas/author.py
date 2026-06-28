from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# --- Request Schemas ---

class AuthorCreate(BaseModel):
    """Schema para criação de autor."""
    name: str
    bio: Optional[str] = None


# --- Response Schemas ---

class AuthorBase(BaseModel):
    """Schema base de resposta do autor."""
    id: int
    name: str
    bio: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthorResponse(AuthorBase):
    """Schema de resposta do autor (sem livros)."""
    pass


class AuthorWithBooksResponse(AuthorBase):
    """Schema de resposta do autor com lista de livros."""
    books: List["BookBasicResponse"] = []


# Importação circular resolvida com update_forward_refs
from app.schemas.book import BookBasicResponse  # noqa: E402

AuthorWithBooksResponse.model_rebuild()
