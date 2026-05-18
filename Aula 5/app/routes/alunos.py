from fastapi import APIRouter, Request
from typing import List
from app.schemas.aluno import AlunoCreate, AlunoPatch, AlunoResponse
from app.services import aluno_service

router = APIRouter(prefix="/api/v1/alunos", tags=["alunos"])

@router.post("", response_model=AlunoResponse, status_code=201)
async def criar_aluno(aluno: AlunoCreate, request: Request):
    return await aluno_service.criar_aluno(request.state.db, aluno)

@router.get("", response_model=List[AlunoResponse])
async def listar_alunos(request: Request):
    return await aluno_service.listar_alunos(request.state.db)

@router.get("/{alunos_id}", response_model=AlunoResponse)
async def buscar_por_id(alunos_id: str, request: Request):
    return await aluno_service.buscar_por_id(request.state.db, alunos_id)

@router.patch("/{alunos_id}", response_model=AlunoResponse)
async def atualizar_aluno(alunos_id: str, aluno: AlunoPatch, request: Request):
    return await aluno_service.atualizar_aluno(request.state.db, alunos_id, aluno)

@router.delete("/{alunos_id}")
async def excluir_aluno(alunos_id: str, request: Request):
    return await aluno_service.excluir_aluno(request.state.db, alunos_id)

@router.delete("")
async def resetar_alunos(request: Request):
    return await aluno_service.resetar_alunos(request.state.db)

@router.delete("/test/reset-all", include_in_schema=False)
async def resetar_tudo_para_testes(request: Request):
    return await aluno_service.resetar_tudo_para_testes(request.state.db)
