from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal, Base
from app.models import User, Author, Book, Category, book_categories  # noqa: F401
from app.seed import seed_categories
from app.routers import auth, books, authors, categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Evento de startup: cria as tabelas e executa o seed."""
    print("Iniciando aplicação...")
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

    # Seed das categorias iniciais
    print("Executando seed de categorias...")
    db = SessionLocal()
    try:
        seed_categories(db)
    finally:
        db.close()

    yield

    print("Encerrando aplicação...")


# Instância do FastAPI
app = FastAPI(
    title="Sistema de Biblioteca",
    description="API para gerenciamento de uma biblioteca com CRUD de livros, autores e categorias.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuração do CORS — permite requests do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint raiz — verifica se a API está funcionando."""
    return {
        "message": "Sistema de Biblioteca API",
        "version": "1.0.0",
        "docs": "/docs",
    }

