CREATE TABLE IF NOT EXISTS Personagem (
    id_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('PC', 'NPC')),
    descricao VARCHAR(200)
);