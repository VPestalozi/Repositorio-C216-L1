from pydantic import BaseModel
from typing import Optional

class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoPatch(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

class AlunoResponse(BaseModel):
    id: str
    nome: str
    email: str
    curso: str
    matricula: int
