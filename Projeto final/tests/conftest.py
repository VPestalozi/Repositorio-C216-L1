"""
conftest.py — Fixtures compartilhadas para os testes.
Usa SQLite em memória para não depender do PostgreSQL durante os testes.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import User, Author, Book, Category, book_categories  # noqa: F401
from app.services.auth import hash_password, create_access_token


# Engine SQLite em memória para testes
SQLALCHEMY_TEST_URL = "sqlite://"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    """Override da dependency get_db para usar o banco de testes."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Substituir a dependency do banco real pelo banco de testes
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Cria as tabelas antes de cada teste e remove após."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client():
    """Retorna um TestClient do FastAPI."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Retorna uma sessão do banco de testes."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def auth_token(db_session):
    """Cria um usuário de teste e retorna o token JWT para autenticação."""
    user = User(
        username="admin_test",
        email="admin@test.com",
        password_hash=hash_password("senha123"),
        is_admin=True,
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(data={"sub": "admin_test"})
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Retorna headers com token JWT para requests autenticados."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def sample_category(db_session):
    """Cria uma categoria de teste."""
    category = Category(name="Ficção Científica", description="Livros de ficção científica")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def sample_author(db_session):
    """Cria um autor de teste."""
    author = Author(name="Isaac Asimov", bio="Escritor de ficção científica")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)
    return author


@pytest.fixture
def sample_book(db_session, sample_author, sample_category):
    """Cria um livro de teste com autor e categoria."""
    book = Book(
        title="Fundação",
        description="Primeiro livro da série Fundação",
        isbn="978-0553293357",
        publication_year=1951,
        author_id=sample_author.id,
    )
    book.categories.append(sample_category)
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book
