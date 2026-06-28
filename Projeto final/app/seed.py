from sqlalchemy.orm import Session
from app.models.category import Category


# Categorias iniciais do sistema
INITIAL_CATEGORIES = [
    {"name": "Romance", "description": "Livros do gênero romance, focados em relacionamentos e emoções."},
    {"name": "Ficção Científica", "description": "Livros de ficção científica, explorando tecnologia, espaço e futuros alternativos."},
    {"name": "Educacional", "description": "Livros educacionais e didáticos para aprendizado e estudo."},
    {"name": "Infantil", "description": "Livros voltados para o público infantil e juvenil."},
    {"name": "Ação", "description": "Livros do gênero ação e aventura, com tramas dinâmicas e emocionantes."},
]


def seed_categories(db: Session) -> None:
    """
    Popula o banco de dados com as categorias iniciais.
    Só insere categorias que ainda não existem.
    """
    for cat_data in INITIAL_CATEGORIES:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            print(f"  ✔ Categoria '{cat_data['name']}' criada.")
        else:
            print(f"  - Categoria '{cat_data['name']}' já existe.")

    db.commit()
    print("Seed de categorias concluído!")
