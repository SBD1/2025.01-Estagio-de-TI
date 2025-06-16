-- Tabela base
CREATE TABLE Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('PowerUp', 'Consumivel', 'Equipamento')),
    preco_base INT NOT NULL DEFAULT 0
);

-- Tabelas especializadas (1 pra 1 com Item)
CREATE TABLE PowerUp (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    bonus_ataque INT,
    duracao INT
);

CREATE TABLE Consumivel (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    recuperacao_vida INT
);

CREATE TABLE Equipamento (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    slot VARCHAR(50),
    bonus_permanente INT
);


-- Tabela para instâncias de itens (drops, itens em inventário, etc)
CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia SERIAL PRIMARY KEY,
    id_item INT REFERENCES Item(id_item),
    quantidade INT DEFAULT 1,
    local_atual VARCHAR(20) CHECK (local_atual IN ('Inventario', 'Chao', 'Loja'))
);
