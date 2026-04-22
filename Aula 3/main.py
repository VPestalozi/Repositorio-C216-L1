from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List # Para usar List no modelo de resposta

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
    curso: str


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    curso: Optional[str] = None


class AlunoResponse(BaseModel):
    matricula: str
    nome: str
    curso: str
    nome_curso: str


class AlunoPatch(BaseModel):
    nome: Optional[str] = None


def gerar_matricula(curso: str) -> str:
    contadores[curso.upper()] += 1
    return f"{curso.upper()}{contadores[curso.upper()]}"


def validar_curso(curso: str) -> bool:
    return curso.upper() in contadores


# POST - Criar um novo aluno
@app.post("/alunos", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoCreate):
    if not aluno.nome or not aluno.nome.strip():
        raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
    
    if not validar_curso(aluno.curso):
        raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
    
    matricula = gerar_matricula(aluno.curso)
    
    alunos[matricula] = {
        "nome": aluno.nome.strip(),
        "curso": aluno.curso.upper(),
        "nome_curso": nomes_cursos[aluno.curso.upper()]
    }
    
    return AlunoResponse(
        matricula=matricula,
        nome=alunos[matricula]["nome"],
        curso=alunos[matricula]["curso"],
        nome_curso=alunos[matricula]["nome_curso"]
    )


# GET - Listar todos os alunos
@app.get("/alunos", response_model=List[AlunoResponse])
def listar_alunos():
    return [
        AlunoResponse(
            matricula=matricula,
            nome=dados["nome"],
            curso=dados["curso"],
            nome_curso=dados["nome_curso"]
        )
        for matricula, dados in sorted(alunos.items())
    ]


# GET - Buscar aluno por matrícula
@app.get("/alunos/{matricula}", response_model=AlunoResponse)
def buscar_por_matricula(matricula: str):
    matricula = matricula.upper()
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com matrícula {matricula} não encontrado.")
    
    return AlunoResponse(
        matricula=matricula,
        nome=alunos[matricula]["nome"],
        curso=alunos[matricula]["curso"],
        nome_curso=alunos[matricula]["nome_curso"]
    )


# GET - Listar alunos por curso
@app.get("/alunos/curso/{curso}", response_model=List[AlunoResponse])
def listar_por_curso(curso: str):
    curso = curso.upper()
    if curso not in contadores:
        raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
    
    resultados = [
        AlunoResponse(
            matricula=matricula,
            nome=dados["nome"],
            curso=dados["curso"],
            nome_curso=dados["nome_curso"]
        )
        for matricula, dados in alunos.items()
        if dados["curso"] == curso
    ]
    
    return resultados


# PUT - Atualizar aluno pela matrícula
@app.put("/alunos/{matricula}", response_model=AlunoResponse)
def atualizar_aluno(matricula: str, aluno: AlunoUpdate):
    matricula = matricula.upper()
    
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com matrícula {matricula} não encontrado.")
    
    if aluno.nome is not None:
        if not aluno.nome.strip():
            raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
        alunos[matricula]["nome"] = aluno.nome.strip()
    
    if aluno.curso is not None:
        if not validar_curso(aluno.curso):
            raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
        
        antigo = alunos.pop(matricula)
        nova_matricula = gerar_matricula(aluno.curso)
        
        antigo["curso"] = aluno.curso.upper()
        antigo["nome_curso"] = nomes_cursos[aluno.curso.upper()]
        alunos[nova_matricula] = antigo
        
        return AlunoResponse(
            matricula=nova_matricula,
            nome=antigo["nome"],
            curso=antigo["curso"],
            nome_curso=antigo["nome_curso"]
        )
    
    return AlunoResponse(
        matricula=matricula,
        nome=alunos[matricula]["nome"],
        curso=alunos[matricula]["curso"],
        nome_curso=alunos[matricula]["nome_curso"]
    )


# DELETE - Excluir aluno pela matrícula
@app.delete("/alunos/{matricula}")
def excluir_aluno(matricula: str):
    matricula = matricula.upper()
    
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com matrícula {matricula} não encontrado.")
    
    aluno_excluido = alunos.pop(matricula)
    
    return {"message": f"Aluno {matricula} ({aluno_excluido['nome']}) excluído com sucesso."}


# PATCH - Atualização parcial do nome do aluno
@app.patch("/alunos/{matricula}", response_model=AlunoResponse)
def patch_aluno(matricula: str, aluno: AlunoPatch):
    matricula = matricula.upper()
    
    if matricula not in alunos:
        raise HTTPException(status_code=404, detail=f"Aluno com matrícula {matricula} não encontrado.")
    
    if aluno.nome is not None:
        if not aluno.nome.strip():
            raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
        alunos[matricula]["nome"] = aluno.nome.strip()
    
    return AlunoResponse(
        matricula=matricula,
        nome=alunos[matricula]["nome"],
        curso=alunos[matricula]["curso"],
        nome_curso=alunos[matricula]["nome_curso"]
    )


# Rota raiz
@app.get("/")
def raiz():
    return {"message": "Sistema de Gestão de Alunos - API REST"}