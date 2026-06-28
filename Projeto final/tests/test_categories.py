"""
test_categories.py — Testes dos endpoints de categorias.
"""


def test_create_category(client, auth_headers):
    """Teste 13: Criar uma nova categoria."""
    response = client.post("/categories/", json={
        "name": "Terror",
        "description": "Livros de terror e suspense",
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Terror"
    assert data["description"] == "Livros de terror e suspense"


def test_list_categories(client, sample_category):
    """Teste 14: Listar todas as categorias."""
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(c["name"] == "Ficção Científica" for c in data)


def test_get_books_by_category(client, sample_book, sample_category):
    """Teste 15: Listar livros de uma categoria específica."""
    response = client.get(f"/categories/{sample_category.id}/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Fundação"
