from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Sistema de Gestão de Alunos")

alunos = {}

contadores = {
    "GES": 0,
    "GEC": 0,
    "GET": 0,
    "GEP": 0,
    "ADS": 0,
    "SI": 0,
}

nomes_cursos = {
    "GES": "Engenharia de Software",
    "GEC": "Engenharia de Computação",
    "GET": "Engenharia de Telecomunicações",
    "GEP": "Engenharia de Produção",
    "ADS": "Análise e Desenvolvimento de Sistemas",
    "SI": "Sistemas de Informação",
}

class AlunoCreate(BaseModel):
    nome: str
    email: str
    curso: str

class AlunoPatch(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    curso: Optional[str] = None

class AlunoResponse(BaseModel):
    id: str
    nome: str
    email: str
    curso: str
    matricula: int

def validar_curso(curso: str) -> bool:
    return curso.upper() in contadores

# POST /api/v1/alunos: Cadastra um aluno novo
@app.post("/api/v1/alunos", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoCreate):
    if not aluno.nome or not aluno.nome.strip():
        raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
    if not aluno.email or not aluno.email.strip():
        raise HTTPException(status_code=400, detail="O email não pode estar vazio.")
    
    curso_upper = aluno.curso.upper()
    if not validar_curso(curso_upper):
        raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
    
    contadores[curso_upper] += 1
    matricula = contadores[curso_upper]
    aluno_id = f"{curso_upper}{matricula}"
    
    alunos[aluno_id] = {
        "id": aluno_id,
        "nome": aluno.nome.strip(),
        "email": aluno.email.strip(),
        "curso": curso_upper,
        "matricula": matricula
    }
    
    return alunos[aluno_id]

# GET /api/v1/alunos: Lista todos os alunos
@app.get("/api/v1/alunos", response_model=List[AlunoResponse])
def listar_alunos():
    return list(alunos.values())

# GET /api/v1/alunos/{alunos_id}: Busca um aluno pelo ID
@app.get("/api/v1/alunos/{alunos_id}", response_model=AlunoResponse)
def buscar_por_id(alunos_id: str):
    alunos_id = alunos_id.upper()
    if alunos_id not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
    return alunos[alunos_id]

# PATCH /api/v1/alunos/{alunos_id}: Atualiza dados de um aluno
@app.patch("/api/v1/alunos/{alunos_id}", response_model=AlunoResponse)
def atualizar_aluno(alunos_id: str, aluno: AlunoPatch):
    alunos_id = alunos_id.upper()
    if alunos_id not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
    
    aluno_atual = alunos[alunos_id]

    if aluno.nome is not None:
        if not aluno.nome.strip():
            raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
        aluno_atual["nome"] = aluno.nome.strip()
        
    if aluno.email is not None:
        if not aluno.email.strip():
            raise HTTPException(status_code=400, detail="O email não pode estar vazio.")
        aluno_atual["email"] = aluno.email.strip()
        
    if aluno.curso is not None:
        curso_upper = aluno.curso.upper()
        if not validar_curso(curso_upper):
            raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
        
        if curso_upper != aluno_atual["curso"]:
            contadores[curso_upper] += 1
            nova_matricula = contadores[curso_upper]
            novo_id = f"{curso_upper}{nova_matricula}"
            
            aluno_atual["curso"] = curso_upper
            aluno_atual["matricula"] = nova_matricula
            aluno_atual["id"] = novo_id
            
            alunos[novo_id] = aluno_atual
            del alunos[alunos_id]
            alunos_id = novo_id
            
    return alunos[alunos_id]

# DELETE /api/v1/alunos/{alunos_id}: Remove um aluno do sistema
@app.delete("/api/v1/alunos/{alunos_id}")
def excluir_aluno(alunos_id: str):
    alunos_id = alunos_id.upper()
    if alunos_id not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
    
    aluno_excluido = alunos.pop(alunos_id)
    return {"message": f"Aluno com ID {alunos_id} ({aluno_excluido['nome']}) removido com sucesso."}

# DELETE /api/v1/alunos: Reseta a lista de alunos
@app.delete("/api/v1/alunos")
def resetar_alunos():
    alunos.clear()
    # Não resetamos os contadores para garantir que os IDs não sejam reutilizados
    return {"message": "Lista de alunos resetada com sucesso."}

# Rota raiz
@app.get("/")
def raiz():
    return {"message": "Sistema de Gestão de Alunos - API REST"}