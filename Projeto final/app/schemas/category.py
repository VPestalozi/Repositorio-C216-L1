from pydantic import BaseModel
from typing import Optional


# --- Request Schemas ---

class CategoryCreate(BaseModel):
    """Schema para criação de categoria."""
    name: str
    description: Optional[str] = None


# --- Response Schemas ---

class CategoryResponse(BaseModel):
    """Schema de resposta da categoria."""
    id: int
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
