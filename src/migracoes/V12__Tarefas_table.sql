CREATE TABLE IF NOT EXISTS Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    dialogo_inicial TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Combate', 'Entrega', 'Conversa')),
    xp_recompensa INT NOT NULL,
    moedas_recompensa INT NOT NULL,
    npc_origem INT NOT NULL,
    FOREIGN KEY (npc_origem) REFERENCES NPC(id_npc)
);

CREATE TABLE IF NOT EXISTS MissaoCombate (

    id_missao INT PRIMARY KEY,
    id_inimigo INT NOT NULL,
    quantidade_alvo INT NOT NULL,
    quantidade_atual INT DEFAULT 0,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);

-- Tabela específica para missões de conversa
CREATE TABLE IF NOT EXISTS MissaoConversa (
    id_missao INT PRIMARY KEY,
    id_npc_alvo INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_npc_alvo) REFERENCES NPC(id_npc)
);



-- Tabela específica para missões de entrega
CREATE TABLE IF NOT EXISTS MissaoEntrega (
    id_missao INT PRIMARY KEY,
    id_item INT NOT NULL,
    quantidade INT NOT NULL,
    id_npc_destino INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_item) REFERENCES Item(id_item),
    FOREIGN KEY (id_npc_destino) REFERENCES NPC(id_npc)
);

CREATE TABLE IF NOT EXISTS MissaoStatus (
    id_missao INT,
    id_estagiario INT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Disponível', 'Em Andamento', 'Concluída')),
    PRIMARY KEY (id_missao, id_estagiario),
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);
