from fastapi.testclient import TestClient
from main import app, alunos, contadores, nomes_cursos

client = TestClient(app)

def setup_function():
    """Reseta os dados antes de cada teste."""
    alunos.clear()
    for key in contadores:
        contadores[key] = 0

def test_criar_aluno_sucesso():
    response = client.post(
        "/alunos",
        json={"nome": "João Silva", "curso": "GES"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["curso"] == "GES"
    assert data["matricula"] == "GES1"
    assert data["nome_curso"] == "Engenharia de Software"


def test_criar_aluno_nome_vazio():
    response = client.post(
        "/alunos",
        json={"nome": "", "curso": "GES"}
    )
    assert response.status_code == 400


def test_criar_aluno_curso_invalido():
    response = client.post(
        "/alunos",
        json={"nome": "João Silva", "curso": "XYZ"}
    )
    assert response.status_code == 400
    assert "Curso inválido" in response.json()["detail"]


def test_criar_aluno_sem_curso():
    response = client.post(
        "/alunos",
        json={"nome": "João Silva"}
    )
    assert response.status_code == 422


def test_listar_alunos_vazio():
    response = client.get("/alunos")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_alunos_com_dados():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    client.post("/alunos", json={"nome": "Maria Santos", "curso": "GEC"})
    
    response = client.get("/alunos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # O sorted() ordena alfabeticamente, então GEC1 vem antes de GES1
    matriculas = [aluno["matricula"] for aluno in data]
    assert "GES1" in matriculas
    assert "GEC1" in matriculas


def test_buscar_por_matricula_sucesso():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.get("/alunos/GES1")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["matricula"] == "GES1"


def test_buscar_por_matricula_nao_encontrada():
    response = client.get("/alunos/GES999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_listar_por_curso_sucesso():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    client.post("/alunos", json={"nome": "Maria Santos", "curso": "GES"})
    client.post("/alunos", json={"nome": "Pedro Costa", "curso": "GEC"})
    
    response = client.get("/alunos/curso/GES")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_listar_por_curso_vazio():
    response = client.get("/alunos/curso/GES")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_por_curso_invalido():
    response = client.get("/alunos/curso/XYZ")
    assert response.status_code == 400
    assert "Curso inválido" in response.json()["detail"]


def test_atualizar_aluno_nao_encontrado():
    response = client.put(
        "/alunos/GES999",
        json={"nome": "Novo Nome"}
    )
    assert response.status_code == 404


def test_atualizar_nome_aluno():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.put(
        "/alunos/GES1",
        json={"nome": "João Santos"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Santos"
    assert data["matricula"] == "GES1"


def test_atualizar_curso_aluno():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.put(
        "/alunos/GES1",
        json={"curso": "GEC"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["curso"] == "GEC"
    assert data["matricula"] == "GEC1"


def test_atualizar_nome_vazio():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.put(
        "/alunos/GES1",
        json={"nome": ""}
    )
    assert response.status_code == 400


def test_excluir_aluno_sucesso():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.delete("/alunos/GES1")
    assert response.status_code == 200
    assert "excluído com sucesso" in response.json()["message"]
    
    response = client.get("/alunos/GES1")
    assert response.status_code == 404


def test_excluir_aluno_nao_encontrado():
    response = client.delete("/alunos/GES999")
    assert response.status_code == 404


def test_patch_aluno_sucesso():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.patch(
        "/alunos/GES1",
        json={"nome": "João Atualizado"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Atualizado"


def test_patch_aluno_nao_encontrado():
    response = client.patch(
        "/alunos/GES999",
        json={"nome": "Novo Nome"}
    )
    assert response.status_code == 404


def test_patch_aluno_nome_vazio():
    client.post("/alunos", json={"nome": "João Silva", "curso": "GES"})
    
    response = client.patch(
        "/alunos/GES1",
        json={"nome": ""}
    )
    assert response.status_code == 400


def test_rota_raiz():
    response = client.get("/")
    assert response.status_code == 200
    assert "Sistema de Gestão de Alunos" in response.json()["message"]