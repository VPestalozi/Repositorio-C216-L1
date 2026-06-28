from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.category import CategoryResponse


# --- Request Schemas ---

class BookCreate(BaseModel):
    """Schema para criação de livro."""
    title: str
    description: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    author_id: Optional[int] = None
    category_ids: List[int] = []


class BookUpdate(BaseModel):
    """Schema para atualização de livro (todos os campos opcionais)."""
    title: Optional[str] = None
    description: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    author_id: Optional[int] = None
    category_ids: Optional[List[int]] = None


# --- Response Schemas ---

class AuthorBasicResponse(BaseModel):
    """Schema básico do autor para uso dentro de BookResponse."""
    id: int
    name: str

    model_config = {"from_attributes": True}


class BookBasicResponse(BaseModel):
    """Schema básico do livro (sem autor detalhado, para evitar referência circular)."""
    id: int
    title: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class BookResponse(BaseModel):
    """Schema completo de resposta do livro."""
    id: int
    title: str
    description: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    author: Optional[AuthorBasicResponse] = None
    categories: List[CategoryResponse] = []

    model_config = {"from_attributes": True}
