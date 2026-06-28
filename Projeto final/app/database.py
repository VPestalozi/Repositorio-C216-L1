from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Criação do engine do SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Sessão local para interações com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()


def get_db():
    """Dependency que fornece uma sessão do banco de dados para cada request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
