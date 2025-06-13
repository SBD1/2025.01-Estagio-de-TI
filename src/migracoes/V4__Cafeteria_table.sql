CREATE TABLE IF NOT EXISTS Cafeteria (
    id_cafeteria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL DEFAULT 'Café do Estágio',
    aberto BOOLEAN NOT NULL DEFAULT TRUE,
    descricao TEXT
);