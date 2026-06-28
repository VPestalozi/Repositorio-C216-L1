/**
 * dashboard.js — Lógica do dashboard (listar e pesquisar livros).
 */

// Verificar autenticação
requireAuth();
showCurrentUser();

// Carregar dados ao iniciar
document.addEventListener("DOMContentLoaded", () => {
    loadBooks();
    loadCategoriesFilter();
});

/**
 * Carrega todos os livros e exibe na tabela.
 */
async function loadBooks() {
    try {
        const response = await apiRequest("/books?limit=100");
        if (response.ok) {
            const books = await response.json();
            renderBooks(books);
        } else {
            showMessage("dashboard-message", "Erro ao carregar livros", "error");
        }
    } catch (err) {
        showMessage("dashboard-message", "Erro de conexão com o servidor", "error");
    }
}

/**
 * Pesquisa livros com filtros.
 */
async function searchBooks() {
    const title = document.getElementById("search-title").value;
    const authorName = document.getElementById("search-author").value;
    const categorySelect = document.getElementById("search-category");
    const category = categorySelect.value;

    let endpoint = "/books/search?";
    const params = [];

    if (title) params.push(`title=${encodeURIComponent(title)}`);
    if (authorName) params.push(`author_name=${encodeURIComponent(authorName)}`);
    if (category) params.push(`category=${encodeURIComponent(category)}`);

    endpoint += params.join("&");

    try {
        const response = await apiRequest(endpoint);
        if (response.ok) {
            const books = await response.json();
            renderBooks(books);
            if (books.length === 0) {
                showMessage("dashboard-message", "Nenhum livro encontrado para os filtros aplicados", "error");
            }
        } else {
            showMessage("dashboard-message", "Erro na pesquisa", "error");
        }
    } catch (err) {
        showMessage("dashboard-message", "Erro de conexão com o servidor", "error");
    }
}

/**
 * Carrega categorias para o filtro de pesquisa.
 */
async function loadCategoriesFilter() {
    try {
        const response = await apiRequest("/categories");
        if (response.ok) {
            const categories = await response.json();
            const select = document.getElementById("search-category");
            categories.forEach(cat => {
                const option = document.createElement("option");
                option.value = cat.name;
                option.textContent = cat.name;
                select.appendChild(option);
            });
        }
    } catch (err) {
        // Silenciar erro no filtro
    }
}

/**
 * Renderiza livros na tabela.
 */
function renderBooks(books) {
    const tbody = document.getElementById("books-tbody");

    if (books.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum livro cadastrado</td></tr>';
        return;
    }

    tbody.innerHTML = books.map(book => `
        <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author ? `<a href="/author/${book.author.id}">${book.author.name}</a>` : '<span class="text-muted">—</span>'}</td>
            <td>${book.isbn || '<span class="text-muted">—</span>'}</td>
            <td>${book.publication_year || '<span class="text-muted">—</span>'}</td>
            <td>${book.categories.map(c => `<span class="tag">${c.name}</span>`).join(" ")}</td>
        </tr>
    `).join("");
}
