from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    """Modelo de categoria de livros (Romance, Ficção Científica, etc.)."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relação N:M — uma categoria tem vários livros (via tabela associativa)
    books = relationship("Book", secondary="book_categories", back_populates="categories")
