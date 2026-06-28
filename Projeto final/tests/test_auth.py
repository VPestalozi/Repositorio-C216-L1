"""
test_auth.py — Testes dos endpoints de autenticação (registro e login).
"""


def test_register_user(client):
    """Teste 1: Registrar um novo usuário com sucesso."""
    response = client.post("/auth/register", json={
        "username": "usuario1",
        "email": "usuario1@email.com",
        "password": "minhasenha123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "usuario1"
    assert data["email"] == "usuario1@email.com"
    assert data["is_admin"] is True
    assert "id" in data
    # Senha não deve aparecer na resposta
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_username(client):
    """Teste 2: Tentativa de registro com username duplicado deve falhar."""
    # Registrar primeiro usuário
    client.post("/auth/register", json={
        "username": "duplicado",
        "email": "email1@email.com",
        "password": "senha123",
    })

    # Tentar registrar com mesmo username
    response = client.post("/auth/register", json={
        "username": "duplicado",
        "email": "email2@email.com",
        "password": "senha456",
    })
    assert response.status_code == 400
    assert "já está em uso" in response.json()["detail"]


def test_login_success(client):
    """Teste 3: Login com credenciais válidas retorna token JWT."""
    # Registrar usuário
    client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@email.com",
        "password": "senhasegura",
    })

    # Fazer login
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "senhasegura",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """Teste 4: Login com senha errada retorna 401."""
    # Registrar usuário
    client.post("/auth/register", json={
        "username": "senhaerrada",
        "email": "erro@email.com",
        "password": "senhacorreta",
    })

    # Tentar login com senha errada
    response = client.post("/auth/login", json={
        "username": "senhaerrada",
        "password": "senhaincorreta",
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"
