/**
 * api.js — Cliente HTTP para comunicação com a API FastAPI.
 * Gerencia token JWT e funções de fetch genéricas.
 */

const API_BASE_URL = "http://localhost:8000";

/**
 * Salva o token JWT no localStorage.
 */
function saveToken(token) {
    localStorage.setItem("access_token", token);
}

/**
 * Retorna o token JWT salvo.
 */
function getToken() {
    return localStorage.getItem("access_token");
}

/**
 * Remove o token JWT (logout).
 */
function removeToken() {
    localStorage.removeItem("access_token");
}

/**
 * Verifica se o usuário está autenticado.
 */
function isAuthenticated() {
    return !!getToken();
}

/**
 * Redireciona para login se não autenticado.
 */
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = "/";
    }
}

/**
 * Logout — remove token e redireciona para login.
 */
function logout() {
    removeToken();
    window.location.href = "/";
}

/**
 * Faz uma requisição à API com headers de autenticação.
 * @param {string} endpoint - Ex: "/books"
 * @param {object} options - Opções do fetch (method, body, etc.)
 * @returns {Promise<Response>}
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers,
    });

    return response;
}

/**
 * Mostra uma mensagem na tela (sucesso ou erro).
 * @param {string} elementId - ID do elemento de mensagem
 * @param {string} text - Texto da mensagem
 * @param {string} type - "success" ou "error"
 */
function showMessage(elementId, text, type = "error") {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = text;
        el.className = `message ${type}`;
        el.classList.remove("hidden");
        setTimeout(() => el.classList.add("hidden"), 5000);
    }
}

/**
 * Exibe o nome do usuário na navbar (decodifica o JWT).
 */
function showCurrentUser() {
    const token = getToken();
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split(".")[1]));
            const userEl = document.getElementById("nav-user");
            if (userEl) {
                userEl.textContent = `👤 ${payload.sub}`;
            }
        } catch (e) {
            // Token inválido
        }
    }
}
