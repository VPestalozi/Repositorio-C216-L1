/**
 * manage.js — Lógica de gerenciamento (CRUD de categorias, autores e livros).
 */

// Verificar autenticação
requireAuth();
showCurrentUser();

// Carregar dados ao iniciar
document.addEventListener("DOMContentLoaded", () => {
    loadCategories();
    loadAuthors();
    loadManageBooks();
});

// ========== CATEGORIAS ==========

/**
 * Carrega e exibe categorias como tags e popula o select de livros.
 */
async function loadCategories() {
    try {
        const response = await apiRequest("/categories");
        if (response.ok) {
            const categories = await response.json();
            renderCategoryTags(categories);
            populateCategorySelect(categories);
        }
    } catch (err) {
        showMessage("manage-message", "Erro ao carregar categorias", "error");
    }
}

function renderCategoryTags(categories) {
    const container = document.getElementById("categories-list");
    if (categories.length === 0) {
        container.innerHTML = '<span class="text-muted">Nenhuma categoria cadastrada</span>';
        return;
    }
    container.innerHTML = categories.map(c =>
        `<span class="tag">${c.name}</span>`
    ).join("");
}

function populateCategorySelect(categories) {
    const select = document.getElementById("book-categories");
    select.innerHTML = "";
    categories.forEach(cat => {
        const option = document.createElement("option");
        option.value = cat.id;
        option.textContent = cat.name;
        select.appendChild(option);
    });
}

/**
 * Cadastra uma nova categoria.
 */
async function handleCreateCategory(event) {
    event.preventDefault();

    const name = document.getElementById("cat-name").value;
    const description = document.getElementById("cat-description").value;

    try {
        const response = await apiRequest("/categories", {
            method: "POST",
            body: JSON.stringify({ name, description: description || null }),
        });

        if (response.ok) {
            showMessage("manage-message", `Categoria "${name}" criada com sucesso!`, "success");
            document.getElementById("category-form").reset();
            loadCategories();
        } else {
            const error = await response.json();
            showMessage("manage-message", error.detail || "Erro ao criar categoria", "error");
        }
    } catch (err) {
        showMessage("manage-message", "Erro de conexão com o servidor", "error");
    }
}

// ========== AUTORES ==========

/**
 * Carrega e exibe autores na tabela e popula o select de livros.
 */
async function loadAuthors() {
    try {
        const response = await apiRequest("/authors");
        if (response.ok) {
            const authors = await response.json();
            renderAuthorsTable(authors);
            populateAuthorSelect(authors);
        }
    } catch (err) {
        showMessage("manage-message", "Erro ao carregar autores", "error");
    }
}

function renderAuthorsTable(authors) {
    const tbody = document.getElementById("authors-tbody");
    if (authors.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">Nenhum autor cadastrado</td></tr>';
        return;
    }
    tbody.innerHTML = authors.map(a => `
        <tr>
            <td>${a.id}</td>
            <td><a href="/author/${a.id}">${a.name}</a></td>
            <td>
                <a href="/author/${a.id}" class="btn btn-xs btn-outline">Ver Livros</a>
            </td>
        </tr>
    `).join("");
}

function populateAuthorSelect(authors) {
    const select = document.getElementById("book-author");
    // Manter a primeira opção "Sem autor"
    select.innerHTML = '<option value="">Sem autor definido</option>';
    authors.forEach(a => {
        const option = document.createElement("option");
        option.value = a.id;
        option.textContent = a.name;
        select.appendChild(option);
    });
}

/**
 * Cadastra um novo autor.
 */
async function handleCreateAuthor(event) {
    event.preventDefault();

    const name = document.getElementById("author-name").value;
    const bio = document.getElementById("author-bio").value;

    try {
        const response = await apiRequest("/authors", {
            method: "POST",
            body: JSON.stringify({ name, bio: bio || null }),
        });

        if (response.ok) {
            showMessage("manage-message", `Autor "${name}" cadastrado com sucesso!`, "success");
            document.getElementById("author-form").reset();
            loadAuthors();
        } else {
            const error = await response.json();
            showMessage("manage-message", error.detail || "Erro ao criar autor", "error");
        }
    } catch (err) {
        showMessage("manage-message", "Erro de conexão com o servidor", "error");
    }
}

// ========== LIVROS ==========

/**
 * Carrega e exibe livros na tabela de gerenciamento.
 */
async function loadManageBooks() {
    try {
        const response = await apiRequest("/books?limit=100");
        if (response.ok) {
            const books = await response.json();
            renderManageBooksTable(books);
        }
    } catch (err) {
        showMessage("manage-message", "Erro ao carregar livros", "error");
    }
}

function renderManageBooksTable(books) {
    const tbody = document.getElementById("manage-books-tbody");
    if (books.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhum livro cadastrado</td></tr>';
        return;
    }
    tbody.innerHTML = books.map(book => `
        <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author ? book.author.name : '<span class="text-muted">—</span>'}</td>
            <td>${book.categories.map(c => `<span class="tag">${c.name}</span>`).join(" ")}</td>
            <td>
                <button class="btn btn-xs btn-outline" onclick="editBook(${book.id})">Editar</button>
                <button class="btn btn-xs btn-danger" onclick="deleteBook(${book.id}, '${book.title.replace(/'/g, "\\'")}')">Excluir</button>
            </td>
        </tr>
    `).join("");
}

/**
 * Handler do formulário de livros (cadastro e edição).
 */
async function handleBookSubmit(event) {
    event.preventDefault();

    const editId = document.getElementById("book-edit-id").value;
    const isEditing = editId !== "";

    const title = document.getElementById("book-title").value;
    const description = document.getElementById("book-description").value;
    const isbn = document.getElementById("book-isbn").value;
    const year = document.getElementById("book-year").value;
    const authorId = document.getElementById("book-author").value;

    // Coletar categorias selecionadas
    const categorySelect = document.getElementById("book-categories");
    const categoryIds = Array.from(categorySelect.selectedOptions).map(opt => parseInt(opt.value));

    if (categoryIds.length === 0) {
        showMessage("manage-message", "Selecione pelo menos uma categoria!", "error");
        return;
    }

    const bookData = {
        title,
        description: description || null,
        isbn: isbn || null,
        publication_year: year ? parseInt(year) : null,
        author_id: authorId ? parseInt(authorId) : null,
        category_ids: categoryIds,
    };

    try {
        let response;
        if (isEditing) {
            response = await apiRequest(`/books/${editId}`, {
                method: "PUT",
                body: JSON.stringify(bookData),
            });
        } else {
            response = await apiRequest("/books", {
                method: "POST",
                body: JSON.stringify(bookData),
            });
        }

        if (response.ok) {
            const action = isEditing ? "atualizado" : "cadastrado";
            showMessage("manage-message", `Livro "${title}" ${action} com sucesso!`, "success");
            document.getElementById("book-form").reset();
            document.getElementById("book-edit-id").value = "";
            document.getElementById("book-submit-btn").textContent = "Cadastrar Livro";
            document.getElementById("book-cancel-btn").classList.add("hidden");
            loadManageBooks();
        } else {
            const error = await response.json();
            showMessage("manage-message", error.detail || "Erro ao salvar livro", "error");
        }
    } catch (err) {
        showMessage("manage-message", "Erro de conexão com o servidor", "error");
    }
}

/**
 * Carrega dados de um livro para edição.
 */
async function editBook(bookId) {
    try {
        const response = await apiRequest(`/books/${bookId}`);
        if (response.ok) {
            const book = await response.json();

            document.getElementById("book-edit-id").value = book.id;
            document.getElementById("book-title").value = book.title;
            document.getElementById("book-description").value = book.description || "";
            document.getElementById("book-isbn").value = book.isbn || "";
            document.getElementById("book-year").value = book.publication_year || "";
            document.getElementById("book-author").value = book.author ? book.author.id : "";

            // Selecionar categorias
            const categorySelect = document.getElementById("book-categories");
            const bookCatIds = book.categories.map(c => c.id.toString());
            Array.from(categorySelect.options).forEach(opt => {
                opt.selected = bookCatIds.includes(opt.value);
            });

            document.getElementById("book-submit-btn").textContent = "Atualizar Livro";
            document.getElementById("book-cancel-btn").classList.remove("hidden");

            // Scroll até o formulário
            document.getElementById("book-form").scrollIntoView({ behavior: "smooth" });
        }
    } catch (err) {
        showMessage("manage-message", "Erro ao carregar dados do livro", "error");
    }
}

/**
 * Cancela a edição e limpa o formulário.
 */
function cancelEdit() {
    document.getElementById("book-form").reset();
    document.getElementById("book-edit-id").value = "";
    document.getElementById("book-submit-btn").textContent = "Cadastrar Livro";
    document.getElementById("book-cancel-btn").classList.add("hidden");
}

/**
 * Exclui um livro após confirmação.
 */
async function deleteBook(bookId, bookTitle) {
    if (!confirm(`Tem certeza que deseja excluir o livro "${bookTitle}"?`)) {
        return;
    }

    try {
        const response = await apiRequest(`/books/${bookId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            showMessage("manage-message", `Livro "${bookTitle}" excluído com sucesso!`, "success");
            loadManageBooks();
        } else {
            const error = await response.json();
            showMessage("manage-message", error.detail || "Erro ao excluir livro", "error");
        }
    } catch (err) {
        showMessage("manage-message", "Erro de conexão com o servidor", "error");
    }
}
