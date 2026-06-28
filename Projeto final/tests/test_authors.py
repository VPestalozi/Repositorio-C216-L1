"""
test_authors.py — Testes dos endpoints de autores.
"""


def test_create_author(client, auth_headers):
    """Teste 16: Cadastrar um novo autor."""
    response = client.post("/authors/", json={
        "name": "George Orwell",
        "bio": "Autor de 1984 e A Revolução dos Bichos",
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "George Orwell"
    assert data["bio"] == "Autor de 1984 e A Revolução dos Bichos"


def test_list_authors(client, sample_author):
    """Teste 17: Listar todos os autores."""
    response = client.get("/authors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(a["name"] == "Isaac Asimov" for a in data)


def test_get_author_with_books(client, sample_book, sample_author):
    """Teste 18: Buscar autor por ID com lista de livros."""
    response = client.get(f"/authors/{sample_author.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Isaac Asimov"
    assert len(data["books"]) >= 1
    assert data["books"][0]["title"] == "Fundação"
