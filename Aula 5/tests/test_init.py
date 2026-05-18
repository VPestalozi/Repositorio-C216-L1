import pytest
import os
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.connection import db

# Configuração da URL base (podemos usar app ASGI diretamente pelo httpx.AsyncClient)
# ou se estivermos rodando no docker com o compose "tests", podemos chamar o backend real se preferir,
# mas testar via ASGI é mais rápido se o banco for o mesmo. Aqui usaremos o ASGI transport.
# Porém, a conexão do banco é via lifespan, o httpx AsyncClient suporta isso.

@pytest.fixture(scope="function", autouse=True)
async def init_db():
    await db.connect()
    yield
    await db.disconnect()

@pytest.fixture(scope="function")
async def client(init_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def setup_db(client: AsyncClient):
    """Reseta os dados antes de cada teste chamando o endpoint de teste."""
    # A rota /api/v1/alunos/test/reset-all foi criada para limpar tabelas
    await client.delete("/api/v1/alunos/test/reset-all")

@pytest.mark.asyncio
async def test_criar_alunos_3_por_curso(client: AsyncClient):
    """Testa a criação de pelo menos 3 alunos por curso."""
    cursos = ["GES", "GEC", "GET", "GEP", "ADS", "SI"]
    
    for curso in cursos:
        for i in range(1, 4):
            response = await client.post(
                "/api/v1/alunos",
                json={
                    "nome": f"Aluno {curso} {i}", 
                    "email": f"aluno{i}@{curso.lower()}.com", 
                    "curso": curso
                }
            )
            assert response.status_code == 201
            data = response.json()
            assert data["nome"] == f"Aluno {curso} {i}"
            assert data["email"] == f"aluno{i}@{curso.lower()}.com"
            assert data["curso"] == curso
            assert data["matricula"] == i
            assert data["id"] == f"{curso}{i}"

@pytest.mark.asyncio
async def test_criar_aluno_campos_invalidos(client: AsyncClient):
    """Testa validações na criação de aluno (campos vazios ou inválidos)."""
    response = await client.post("/api/v1/alunos", json={"nome": "", "email": "a@a.com", "curso": "GES"})
    assert response.status_code == 400
    
    response = await client.post("/api/v1/alunos", json={"nome": "João", "email": "", "curso": "GES"})
    assert response.status_code == 400
    
    response = await client.post("/api/v1/alunos", json={"nome": "João", "email": "a@a.com", "curso": "XYZ"})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_listar_alunos(client: AsyncClient):
    """Testa a listagem geral de alunos."""
    await client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    await client.post("/api/v1/alunos", json={"nome": "Maria", "email": "m@a.com", "curso": "GEC"})
    
    response = await client.get("/api/v1/alunos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    ids = [aluno["id"] for aluno in data]
    assert "GES1" in ids
    assert "GEC1" in ids

@pytest.mark.asyncio
async def test_buscar_por_id_sucesso(client: AsyncClient):
    """Testa a busca de aluno específico por ID."""
    await client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = await client.get("/api/v1/alunos/GES1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "GES1"
    assert data["nome"] == "João"

@pytest.mark.asyncio
async def test_buscar_por_id_nao_encontrado(client: AsyncClient):
    response = await client.get("/api/v1/alunos/GES999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_atualizar_dados_patch(client: AsyncClient):
    """Testa a atualização de dados do aluno via PATCH."""
    await client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = await client.patch(
        "/api/v1/alunos/GES1",
        json={"nome": "João Atualizado", "email": "novo@a.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Atualizado"
    assert data["email"] == "novo@a.com"
    assert data["id"] == "GES1"
    
    response_curso = await client.patch(
        "/api/v1/alunos/GES1",
        json={"curso": "GEC"}
    )
    assert response_curso.status_code == 200
    data_curso = response_curso.json()
    assert data_curso["curso"] == "GEC"
    assert data_curso["id"] == "GEC1"
    
    res_ges = await client.get("/api/v1/alunos/GES1")
    assert res_ges.status_code == 404
    
    res_gec = await client.get("/api/v1/alunos/GEC1")
    assert res_gec.status_code == 200

@pytest.mark.asyncio
async def test_remover_aluno(client: AsyncClient):
    """Testa a remoção de um aluno específico."""
    await client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = await client.delete("/api/v1/alunos/GES1")
    assert response.status_code == 200
    assert "removido com sucesso" in response.json()["message"]
    
    res = await client.get("/api/v1/alunos/GES1")
    assert res.status_code == 404

@pytest.mark.asyncio
async def test_resetar_alunos(client: AsyncClient):
    """Testa o reset de todos os alunos cadastrados."""
    await client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    await client.post("/api/v1/alunos", json={"nome": "Maria", "email": "m@a.com", "curso": "GEC"})
    
    response = await client.delete("/api/v1/alunos")
    assert response.status_code == 200
    
    res = await client.get("/api/v1/alunos")
    assert len(res.json()) == 0

@pytest.mark.asyncio
async def test_rota_raiz(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Sistema de Gestão de Alunos" in response.json()["message"]