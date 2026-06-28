from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models.category import Category
from app.models.book import Book
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.book import BookResponse
from app.middlewares.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categorias"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Criar uma nova categoria de livros.
    Requer autenticação.
    """
    # Verificar se a categoria já existe
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria '{category_data.name}' já existe",
        )

    new_category = Category(
        name=category_data.name,
        description=category_data.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """
    Listar todas as categorias disponíveis.
    """
    categories = db.query(Category).order_by(Category.name).all()
    return categories


@router.get("/{category_id}/books", response_model=List[BookResponse])
def get_books_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Listar todos os livros de uma categoria específica.
    Retorna os livros com informações do autor e demais categorias.
    """
    # Verificar se a categoria existe
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID {category_id} não encontrada",
        )

    # Buscar livros desta categoria
    books = (
        db.query(Book)
        .join(Book.categories)
        .options(joinedload(Book.author), joinedload(Book.categories))
        .filter(Category.id == category_id)
        .all()
    )

    # Remover duplicatas dos joins
    seen_ids = set()
    unique_books = []
    for book in books:
        if book.id not in seen_ids:
            seen_ids.add(book.id)
            unique_books.append(book)

    return unique_books
