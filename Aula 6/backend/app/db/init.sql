CREATE TABLE IF NOT EXISTS contadores (
    curso VARCHAR(10) PRIMARY KEY,
    valor INTEGER NOT NULL DEFAULT 0
);

INSERT INTO contadores (curso, valor) VALUES
    ('GES', 0),
    ('GEC', 0),
    ('GET', 0),
    ('GEP', 0),
    ('ADS', 0),
    ('SI', 0)
ON CONFLICT (curso) DO NOTHING;

CREATE TABLE IF NOT EXISTS alunos (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    curso VARCHAR(10) NOT NULL REFERENCES contadores(curso),
    matricula INTEGER NOT NULL
);
