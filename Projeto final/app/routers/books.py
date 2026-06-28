from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.database import get_db
from app.models.book import Book, book_categories
from app.models.author import Author
from app.models.category import Category
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.middlewares.auth import get_current_user

router = APIRouter(prefix="/books", tags=["Livros"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cadastrar um novo livro.
    Permite associar a um autor e a múltiplas categorias.
    Requer autenticação.
    """
    # Verificar se o autor existe (se fornecido)
    if book_data.author_id:
        author = db.query(Author).filter(Author.id == book_data.author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor com ID {book_data.author_id} não encontrado",
            )

    # Verificar se ISBN já existe (se fornecido)
    if book_data.isbn:
        existing_isbn = db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing_isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ISBN '{book_data.isbn}' já está cadastrado",
            )

    # Buscar categorias
    categories = []
    if book_data.category_ids:
        categories = db.query(Category).filter(Category.id.in_(book_data.category_ids)).all()
        if len(categories) != len(book_data.category_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma ou mais categorias não foram encontradas",
            )

    # Criar o livro
    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        isbn=book_data.isbn,
        publication_year=book_data.publication_year,
        author_id=book_data.author_id,
    )
    new_book.categories = categories

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get("/", response_model=List[BookResponse])
def list_books(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros"),
    db: Session = Depends(get_db),
):
    """
    Listar todos os livros com paginação.
    Inclui informações do autor e categorias.
    """
    books = (
        db.query(Book)
        .options(joinedload(Book.author), joinedload(Book.categories))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return books


@router.get("/search", response_model=List[BookResponse])
def search_books(
    title: Optional[str] = Query(None, description="Buscar por título (parcial)"),
    author_name: Optional[str] = Query(None, description="Buscar por nome do autor (parcial)"),
    category: Optional[str] = Query(None, description="Filtrar por nome da categoria"),
    year: Optional[int] = Query(None, description="Filtrar por ano de publicação"),
    db: Session = Depends(get_db),
):
    """
    Pesquisar livros por título, nome do autor, categoria ou ano de publicação.
    Os filtros podem ser combinados.
    """
    query = db.query(Book).options(joinedload(Book.author), joinedload(Book.categories))

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if author_name:
        query = query.join(Author).filter(Author.name.ilike(f"%{author_name}%"))

    if category:
        query = query.join(Book.categories).filter(Category.name.ilike(f"%{category}%"))

    if year:
        query = query.filter(Book.publication_year == year)

    books = query.all()

    # Remover duplicatas que podem surgir dos joins
    seen_ids = set()
    unique_books = []
    for book in books:
        if book.id not in seen_ids:
            seen_ids.add(book.id)
            unique_books.append(book)

    return unique_books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Buscar um livro específico por ID.
    Retorna os detalhes completos com autor e categorias.
    """
    book = (
        db.query(Book)
        .options(joinedload(Book.author), joinedload(Book.categories))
        .filter(Book.id == book_id)
        .first()
    )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {book_id} não encontrado",
        )
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualizar informações de um livro existente.
    Apenas os campos enviados serão atualizados (atualização parcial).
    Requer autenticação.
    """
    book = (
        db.query(Book)
        .options(joinedload(Book.author), joinedload(Book.categories))
        .filter(Book.id == book_id)
        .first()
    )
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {book_id} não encontrado",
        )

    # Atualizar campos fornecidos
    if book_data.title is not None:
        book.title = book_data.title

    if book_data.description is not None:
        book.description = book_data.description

    if book_data.isbn is not None:
        # Verificar se o novo ISBN já existe em outro livro
        existing = db.query(Book).filter(Book.isbn == book_data.isbn, Book.id != book_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ISBN '{book_data.isbn}' já está cadastrado em outro livro",
            )
        book.isbn = book_data.isbn

    if book_data.publication_year is not None:
        book.publication_year = book_data.publication_year

    if book_data.author_id is not None:
        author = db.query(Author).filter(Author.id == book_data.author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor com ID {book_data.author_id} não encontrado",
            )
        book.author_id = book_data.author_id

    if book_data.category_ids is not None:
        categories = db.query(Category).filter(Category.id.in_(book_data.category_ids)).all()
        if len(categories) != len(book_data.category_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma ou mais categorias não foram encontradas",
            )
        book.categories = categories

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Deletar um livro por ID.
    Remove também as associações na tabela book_categories.
    Requer autenticação.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {book_id} não encontrado",
        )

    db.delete(book)
    db.commit()

    return None
