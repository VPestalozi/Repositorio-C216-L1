from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


# Tabela associativa N:M entre livros e categorias
book_categories = Table(
    "book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class Book(Base):
    """Modelo de livro."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(300), nullable=False, index=True)
    description = Column(Text, nullable=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    publication_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # FK — Relação N:1 com autor
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True)

    # Relação N:1 — muitos livros pertencem a um autor
    author = relationship("Author", back_populates="books")

    # Relação N:M — um livro pode ter várias categorias
    categories = relationship("Category", secondary=book_categories, back_populates="books")
