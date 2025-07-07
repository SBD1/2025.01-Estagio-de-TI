-- Tabela para busca itens q existe no jogo
CREATE TABLE Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('PowerUp', 'Consumivel', 'Arma')),
    preco_base INT NOT NULL DEFAULT 0,

    dano INT,        -- para Arma
    recuperacao_vida INT,        -- para Consumivel
    bonus_ataque INT,         -- para PowerUp
    nivel_minimo INT
    
);


-- tabela para instâncias de itens (drops, itens em inventário, etc)
CREATE TABLE InstanciaItem (
    id_instancia SERIAL PRIMARY KEY,
    id_item INT REFERENCES Item(id_item),
    id_npc INT,      
    id_sala INT,
    id_estagiario INT,
    quantidade INT DEFAULT 1,
    local_atual VARCHAR(20) CHECK (local_atual IN ('Inventario', 'Chao', 'Loja')),
    lido BOOLEAN --so para livros
);

