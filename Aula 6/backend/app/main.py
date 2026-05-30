from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.connection import db
from app.middlewares.db_middleware import DBMiddleware
from app.routes import alunos

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ao iniciar
    await db.connect()
    yield
    # Ao desligar
    await db.disconnect()

app = FastAPI(title="Sistema de Gestão de Alunos", lifespan=lifespan)

# Adiciona o middleware
app.add_middleware(DBMiddleware)

# Inclui as rotas
app.include_router(alunos.router)

# Rota raiz
@app.get("/")
def raiz():
    return {"message": "Sistema de Gestão de Alunos - API REST"}
