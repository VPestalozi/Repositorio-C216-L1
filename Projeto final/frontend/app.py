from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def login():
    """Página de login e registro."""
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """Página principal — listagem e pesquisa de livros."""
    return render_template("dashboard.html")


@app.route("/manage")
def manage():
    """Página de gerenciamento — CRUD de categorias, autores e livros."""
    return render_template("manage.html")


@app.route("/author/<int:author_id>")
def author(author_id):
    """Página de detalhes do autor."""
    return render_template("author.html", author_id=author_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002, debug=True)
