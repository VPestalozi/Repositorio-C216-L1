from typing import List, Optional
from asyncpg import Connection
from fastapi import HTTPException
from app.schemas.aluno import AlunoCreate, AlunoPatch

CURSOS_VALIDOS = {"GES", "GEC", "GET", "GEP", "ADS", "SI"}

async def validar_curso(curso: str) -> bool:
    return curso.upper() in CURSOS_VALIDOS

async def criar_aluno(db: Connection, aluno: AlunoCreate) -> dict:
    if not aluno.nome or not aluno.nome.strip():
        raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
    if not aluno.email or not aluno.email.strip():
        raise HTTPException(status_code=400, detail="O email não pode estar vazio.")
    
    curso_upper = aluno.curso.upper()
    if not await validar_curso(curso_upper):
        raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
    
    async with db.transaction():
        # Bloqueia a linha do contador para este curso
        row = await db.fetchrow(
            "SELECT valor FROM contadores WHERE curso = $1 FOR UPDATE", 
            curso_upper
        )
        if not row:
            # Insere caso não exista, embora o init.sql já preencha
            await db.execute("INSERT INTO contadores (curso, valor) VALUES ($1, 0)", curso_upper)
            novo_valor = 1
        else:
            novo_valor = row["valor"] + 1
            
        await db.execute("UPDATE contadores SET valor = $1 WHERE curso = $2", novo_valor, curso_upper)
        
        matricula = novo_valor
        aluno_id = f"{curso_upper}{matricula}"
        
        await db.execute(
            """
            INSERT INTO alunos (id, nome, email, curso, matricula)
            VALUES ($1, $2, $3, $4, $5)
            """,
            aluno_id, aluno.nome.strip(), aluno.email.strip(), curso_upper, matricula
        )
        
        return {
            "id": aluno_id,
            "nome": aluno.nome.strip(),
            "email": aluno.email.strip(),
            "curso": curso_upper,
            "matricula": matricula
        }

async def listar_alunos(db: Connection) -> List[dict]:
    rows = await db.fetch("SELECT * FROM alunos")
    return [dict(row) for row in rows]

async def buscar_por_id(db: Connection, alunos_id: str) -> dict:
    alunos_id = alunos_id.upper()
    row = await db.fetchrow("SELECT * FROM alunos WHERE id = $1", alunos_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
    return dict(row)

async def atualizar_aluno(db: Connection, alunos_id: str, aluno: AlunoPatch) -> dict:
    alunos_id = alunos_id.upper()
    
    async with db.transaction():
        aluno_atual = await db.fetchrow("SELECT * FROM alunos WHERE id = $1 FOR UPDATE", alunos_id)
        if not aluno_atual:
            raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
        
        aluno_atual_dict = dict(aluno_atual)
        
        if aluno.nome is not None:
            if not aluno.nome.strip():
                raise HTTPException(status_code=400, detail="O nome não pode estar vazio.")
            aluno_atual_dict["nome"] = aluno.nome.strip()
            
        if aluno.email is not None:
            if not aluno.email.strip():
                raise HTTPException(status_code=400, detail="O email não pode estar vazio.")
            aluno_atual_dict["email"] = aluno.email.strip()
            
        if aluno.curso is not None:
            curso_upper = aluno.curso.upper()
            if not await validar_curso(curso_upper):
                raise HTTPException(status_code=400, detail="Curso inválido. Escolha um dos códigos: GES, GEC, GET, GEP, ADS, SI")
            
            if curso_upper != aluno_atual_dict["curso"]:
                row = await db.fetchrow("SELECT valor FROM contadores WHERE curso = $1 FOR UPDATE", curso_upper)
                if not row:
                    await db.execute("INSERT INTO contadores (curso, valor) VALUES ($1, 0)", curso_upper)
                    nova_matricula = 1
                else:
                    nova_matricula = row["valor"] + 1
                    
                await db.execute("UPDATE contadores SET valor = $1 WHERE curso = $2", nova_matricula, curso_upper)
                
                novo_id = f"{curso_upper}{nova_matricula}"
                
                # Para evitar problemas com a primary key antiga, inserimos o novo e deletamos o antigo
                # ou atualizamos o ID (já que no Postgres atualizações de PK são permitidas com cascade e não violações)
                # Vamos apenas usar o UPDATE pois alteramos o ID
                
                await db.execute(
                    """
                    UPDATE alunos 
                    SET id = $1, nome = $2, email = $3, curso = $4, matricula = $5
                    WHERE id = $6
                    """,
                    novo_id, aluno_atual_dict["nome"], aluno_atual_dict["email"], curso_upper, nova_matricula, alunos_id
                )
                
                aluno_atual_dict["curso"] = curso_upper
                aluno_atual_dict["matricula"] = nova_matricula
                aluno_atual_dict["id"] = novo_id
                
                return aluno_atual_dict

        # Caso não haja mudança de curso, apenas atualiza nome/email
        await db.execute(
            """
            UPDATE alunos 
            SET nome = $1, email = $2
            WHERE id = $3
            """,
            aluno_atual_dict["nome"], aluno_atual_dict["email"], alunos_id
        )
        
        return aluno_atual_dict

async def excluir_aluno(db: Connection, alunos_id: str) -> dict:
    alunos_id = alunos_id.upper()
    aluno_excluido = await db.fetchrow("SELECT * FROM alunos WHERE id = $1", alunos_id)
    
    if not aluno_excluido:
        raise HTTPException(status_code=404, detail=f"Aluno com ID {alunos_id} não encontrado.")
    
    await db.execute("DELETE FROM alunos WHERE id = $1", alunos_id)
    return {"message": f"Aluno com ID {alunos_id} ({aluno_excluido['nome']}) removido com sucesso."}

async def resetar_alunos(db: Connection) -> dict:
    # Não resetamos os contadores, apenas deletamos os alunos
    await db.execute("DELETE FROM alunos")
    return {"message": "Lista de alunos resetada com sucesso."}

async def resetar_tudo_para_testes(db: Connection) -> dict:
    # Utilizado internamente para os testes
    await db.execute("DELETE FROM alunos")
    await db.execute("UPDATE contadores SET valor = 0")
    return {"message": "Tudo resetado."}
