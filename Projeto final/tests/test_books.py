"""
test_books.py — Testes dos endpoints de livros (CRUD completo).
"""


def test_create_book(client, auth_headers, sample_category, sample_author):
    """Teste 5: Cadastrar um livro com autor e categoria."""
    response = client.post("/books/", json={
        "title": "Duna",
        "description": "Ficção científica clássica",
        "isbn": "978-0441013593",
        "publication_year": 1965,
        "author_id": sample_author.id,
        "category_ids": [sample_category.id],
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Duna"
    assert data["isbn"] == "978-0441013593"
    assert data["publication_year"] == 1965
    assert data["author"]["name"] == "Isaac Asimov"
    assert len(data["categories"]) == 1
    assert data["categories"][0]["name"] == "Ficção Científica"


def test_create_book_without_auth(client, sample_category):
    """Teste 6: Criar livro sem autenticação deve retornar 401."""
    response = client.post("/books/", json={
        "title": "Livro sem auth",
        "category_ids": [sample_category.id],
    })
    assert response.status_code == 401


def test_list_books(client, sample_book):
    """Teste 7: Listar todos os livros cadastrados."""
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Fundação"


def test_get_book_by_id(client, sample_book):
    """Teste 8: Buscar livro por ID."""
    response = client.get(f"/books/{sample_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Fundação"
    assert data["author"]["name"] == "Isaac Asimov"
    assert len(data["categories"]) == 1


def test_get_book_not_found(client):
    """Teste 9: Buscar livro inexistente retorna 404."""
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


def test_update_book(client, auth_headers, sample_book):
    """Teste 10: Atualizar título de um livro."""
    response = client.put(f"/books/{sample_book.id}", json={
        "title": "Fundação — Edição Revisada",
        "publication_year": 2024,
    }, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Fundação — Edição Revisada"
    assert data["publication_year"] == 2024
    # Campos não alterados devem permanecer
    assert data["isbn"] == "978-0553293357"


def test_delete_book(client, auth_headers, sample_book):
    """Teste 11: Deletar um livro por ID."""
    response = client.delete(f"/books/{sample_book.id}", headers=auth_headers)
    assert response.status_code == 204

    # Verificar que o livro foi removido
    response = client.get(f"/books/{sample_book.id}")
    assert response.status_code == 404


def test_search_books_by_title(client, sample_book):
    """Teste 12: Pesquisar livros por título (parcial)."""
    response = client.get("/books/search?title=Fund")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Fundação" in data[0]["title"]
