from fastapi.testclient import TestClient
from main import app, alunos, contadores

client = TestClient(app)

def setup_function():
    """Reseta os dados antes de cada teste."""
    alunos.clear()
    for key in contadores:
        contadores[key] = 0

def test_criar_alunos_3_por_curso():
    """Testa a criação de pelo menos 3 alunos por curso."""
    cursos = ["GES", "GEC", "GET", "GEP", "ADS", "SI"]
    
    for curso in cursos:
        for i in range(1, 4):
            response = client.post(
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

def test_criar_aluno_campos_invalidos():
    """Testa validações na criação de aluno (campos vazios ou inválidos)."""
    response = client.post("/api/v1/alunos", json={"nome": "", "email": "a@a.com", "curso": "GES"})
    assert response.status_code == 400
    
    response = client.post("/api/v1/alunos", json={"nome": "João", "email": "", "curso": "GES"})
    assert response.status_code == 400
    
    response = client.post("/api/v1/alunos", json={"nome": "João", "email": "a@a.com", "curso": "XYZ"})
    assert response.status_code == 400

def test_listar_alunos():
    """Testa a listagem geral de alunos."""
    client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    client.post("/api/v1/alunos", json={"nome": "Maria", "email": "m@a.com", "curso": "GEC"})
    
    response = client.get("/api/v1/alunos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    ids = [aluno["id"] for aluno in data]
    assert "GES1" in ids
    assert "GEC1" in ids

def test_buscar_por_id_sucesso():
    """Testa a busca de aluno específico por ID."""
    client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = client.get("/api/v1/alunos/GES1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "GES1"
    assert data["nome"] == "João"

def test_buscar_por_id_nao_encontrado():
    response = client.get("/api/v1/alunos/GES999")
    assert response.status_code == 404

def test_atualizar_dados_patch():
    """Testa a atualização de dados do aluno via PATCH."""
    client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = client.patch(
        "/api/v1/alunos/GES1",
        json={"nome": "João Atualizado", "email": "novo@a.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Atualizado"
    assert data["email"] == "novo@a.com"
    assert data["id"] == "GES1"
    
    response_curso = client.patch(
        "/api/v1/alunos/GES1",
        json={"curso": "GEC"}
    )
    assert response_curso.status_code == 200
    data_curso = response_curso.json()
    assert data_curso["curso"] == "GEC"
    assert data_curso["id"] == "GEC1"
    
    assert client.get("/api/v1/alunos/GES1").status_code == 404
    assert client.get("/api/v1/alunos/GEC1").status_code == 200

def test_remover_aluno():
    """Testa a remoção de um aluno específico."""
    client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    
    response = client.delete("/api/v1/alunos/GES1")
    assert response.status_code == 200
    assert "removido com sucesso" in response.json()["message"]
    
    assert client.get("/api/v1/alunos/GES1").status_code == 404

def test_resetar_alunos():
    """Testa o reset de todos os alunos cadastrados."""
    client.post("/api/v1/alunos", json={"nome": "João", "email": "j@a.com", "curso": "GES"})
    client.post("/api/v1/alunos", json={"nome": "Maria", "email": "m@a.com", "curso": "GEC"})
    
    response = client.delete("/api/v1/alunos")
    assert response.status_code == 200
    
    assert len(client.get("/api/v1/alunos").json()) == 0

def test_rota_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema de Gestão de Alunos" in response.json()["message"]