from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.author import Author
from app.models.user import User
from app.schemas.author import AuthorCreate, AuthorResponse, AuthorWithBooksResponse
from app.middlewares.auth import get_current_user

router = APIRouter(prefix="/authors", tags=["Autores"])


@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(
    author_data: AuthorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cadastrar um novo autor.
    Requer autenticação.
    """
    new_author = Author(
        name=author_data.name,
        bio=author_data.bio,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


@router.get("/", response_model=List[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    """
    Listar todos os autores cadastrados.
    """
    authors = db.query(Author).order_by(Author.name).all()
    return authors


@router.get("/{author_id}", response_model=AuthorWithBooksResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """
    Buscar um autor por ID, incluindo a lista de seus livros.
    """
    author = (
        db.query(Author)
        .options(joinedload(Author.books))
        .filter(Author.id == author_id)
        .first()
    )
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com ID {author_id} não encontrado",
        )
    return author
