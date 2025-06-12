CREATE TABLE IF NOT EXISTS Mundo (
    id_mundo SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL DEFAULT 'Empresa Tech S/A',
    data_inicio DATE NOT NULL
);