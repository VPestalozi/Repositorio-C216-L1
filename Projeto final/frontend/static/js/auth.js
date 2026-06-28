/**
 * auth.js — Lógica da página de login e registro.
 */

// Redireciona se já autenticado
if (isAuthenticated()) {
    window.location.href = "/dashboard";
}

/**
 * Mostra o formulário de login.
 */
function showLogin() {
    document.getElementById("login-form").classList.remove("hidden");
    document.getElementById("register-form").classList.add("hidden");
    document.getElementById("btn-show-login").classList.add("active");
    document.getElementById("btn-show-register").classList.remove("active");
}

/**
 * Mostra o formulário de registro.
 */
function showRegister() {
    document.getElementById("login-form").classList.add("hidden");
    document.getElementById("register-form").classList.remove("hidden");
    document.getElementById("btn-show-login").classList.remove("active");
    document.getElementById("btn-show-register").classList.add("active");
}

/**
 * Handler do formulário de login.
 */
async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    try {
        const response = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            saveToken(data.access_token);
            window.location.href = "/dashboard";
        } else {
            const error = await response.json();
            showMessage("auth-message", error.detail || "Erro ao fazer login", "error");
        }
    } catch (err) {
        showMessage("auth-message", "Erro de conexão com o servidor", "error");
    }
}

/**
 * Handler do formulário de registro.
 */
async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    try {
        const response = await apiRequest("/auth/register", {
            method: "POST",
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            showMessage("auth-message", "Registro realizado com sucesso! Faça login.", "success");
            showLogin();
            // Limpar formulário de registro
            document.getElementById("register-form").reset();
        } else {
            const error = await response.json();
            showMessage("auth-message", error.detail || "Erro ao registrar", "error");
        }
    } catch (err) {
        showMessage("auth-message", "Erro de conexão com o servidor", "error");
    }
}
