/**
 * author.js — Lógica da página de detalhes do autor.
 * Usa a variável global AUTHOR_ID definida no template Jinja2.
 */

// Verificar autenticação
requireAuth();
showCurrentUser();

// Carregar dados ao iniciar
document.addEventListener("DOMContentLoaded", () => {
    loadAuthorDetails();
});

/**
 * Carrega informações do autor e seus livros.
 */
async function loadAuthorDetails() {
    try {
        const response = await apiRequest(`/authors/${AUTHOR_ID}`);
        if (response.ok) {
            const author = await response.json();
            renderAuthorInfo(author);
            renderAuthorBooks(author.books || []);
        } else {
            showMessage("author-message", "Autor não encontrado", "error");
            document.getElementById("author-name").textContent = "Autor não encontrado";
        }
    } catch (err) {
        showMessage("author-message", "Erro de conexão com o servidor", "error");
    }
}

/**
 * Renderiza informações do autor.
 */
function renderAuthorInfo(author) {
    document.getElementById("author-name").textContent = `✍️ ${author.name}`;
    document.getElementById("author-bio").textContent = author.bio || "Sem biografia cadastrada.";

    const date = new Date(author.created_at);
    document.getElementById("author-date").textContent = `Cadastrado em: ${date.toLocaleDateString("pt-BR")}`;
}

/**
 * Renderiza livros do autor na tabela.
 */
function renderAuthorBooks(books) {
    const tbody = document.getElementById("author-books-tbody");

    if (books.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhum livro cadastrado para este autor</td></tr>';
        return;
    }

    tbody.innerHTML = books.map(book => `
        <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.isbn || '<span class="text-muted">—</span>'}</td>
            <td>${book.publication_year || '<span class="text-muted">—</span>'}</td>
            <td>—</td>
        </tr>
    `).join("");
}
