CREATE TABLE IF NOT EXISTS Mundo (
    id_mundo SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL DEFAULT 'Empresa Tech S/A',
    data_inicio DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Andar (
    id_andar SERIAL PRIMARY KEY,
    id_mundo INT NOT NULL, 
    FOREIGN KEY (id_mundo) REFERENCES Mundo(id_mundo),
    numero SMALLINT NOT NULL, -- -2 = Subsolo 2, -1 = Subsolo 1, 0 = Térreo, 1~10 = Andares
    nome VARCHAR(100) NOT NULL
    
);

CREATE TABLE IF NOT EXISTS Sala (
    id_sala SERIAL PRIMARY KEY,
    id_andar INT NOT NULL,
    bloqueada BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (id_andar) REFERENCES Andar(id_andar),
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ConexaoSala (
    id_sala_origem INT NOT NULL,
    FOREIGN KEY (id_sala_origem) REFERENCES Sala(id_sala),
    
    id_sala_destino INT NOT NULL,
    FOREIGN KEY (id_sala_destino) REFERENCES Sala(id_sala),

    PRIMARY KEY (id_sala_origem, id_sala_destino),
    CHECK (id_sala_origem != id_sala_destino)
);

CREATE TABLE IF NOT EXISTS Cafeteria (
    id_cafeteria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL DEFAULT 'Café do Estágio',
    aberto BOOLEAN NOT NULL DEFAULT TRUE,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS Personagem (
    id_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('PC', 'NPC')),
    descricao VARCHAR(200),
    CONSTRAINT UQ_Personagem_Nome UNIQUE(nome)
);

-- CORREÇÃO: Adicionada a coluna 'sala_atual' para localização exata do NPC.
CREATE TABLE IF NOT EXISTS NPC (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem) ON DELETE CASCADE,
    tipo VARCHAR(20) NOT NULL, -- Ex: 'Chefe', 'Colega', 'Almoxarife'
    andar_atual INT REFERENCES Andar(id_andar),
    sala_atual INT REFERENCES Sala(id_sala), -- <<-- NOVA COLUNA
    dialogo_padrao VARCHAR(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS Estagiario (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem) ON DELETE CASCADE,
    xp INT NOT NULL CHECK (xp BETWEEN 0 AND 10000),
    nivel INT NOT NULL CHECK (nivel >= 1 AND nivel <= 100),
    respeito INT DEFAULT 0 CHECK (respeito >= 0 AND respeito <= 100),
    coins INT NOT NULL DEFAULT 0,
    ataque INT NOT NULL DEFAULT 10,
    defesa INT NOT NULL DEFAULT 5,
    vida INT NOT NULL DEFAULT 100,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Normal', 'Confuso', 'Estressado', 'Motivado')),
    andar_atual INT,
    sala_atual INT,
    FOREIGN KEY (andar_atual) REFERENCES Andar(id_andar),
    FOREIGN KEY (sala_atual) REFERENCES Sala(id_sala)
);

CREATE TABLE IF NOT EXISTS ChefeFinal (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES NPC(id_personagem),
    desafio_final VARCHAR(200) NOT NULL
);

CREATE TABLE Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('PowerUp', 'Consumivel', 'Equipamento')),
    preco_base INT NOT NULL DEFAULT 0
);

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
    bonus_ataque INT DEFAULT 0,
    bonus_defesa INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia SERIAL PRIMARY KEY,
    id_item INT REFERENCES Item(id_item),
    quantidade INT DEFAULT 1,
    local_atual VARCHAR(20) CHECK (local_atual IN ('Inventario', 'Chao', 'Loja'))
);

CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL UNIQUE,
    espaco_total INT NOT NULL DEFAULT 12, 
    espaco_usado INT NOT NULL DEFAULT 0,  
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ItemInventario (
    id_inventario INT,
    id_instancia INT,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_inventario, id_instancia),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario) ON DELETE CASCADE,
    FOREIGN KEY (id_instancia) REFERENCES InstanciaItem(id_instancia) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS EstagiarioEquipamento (
    id_estagiario INT NOT NULL,
    id_instancia INT NOT NULL UNIQUE,
    slot VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_estagiario, slot),
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem) ON DELETE CASCADE,
    FOREIGN KEY (id_instancia) REFERENCES InstanciaItem(id_instancia) ON DELETE CASCADE
);

CREATE TABLE Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ataque VARCHAR(100) NOT NULL
);

-- CORREÇÃO: Adicionada a coluna 'sala_atual' para localização exata do inimigo.
CREATE TABLE InstanciaInimigo (
    id_instancia SERIAL PRIMARY KEY,
    id_inimigo INT NOT NULL,
    vida int NOT NULL,
    dano int NOT NULL,
    sala_atual INT REFERENCES Sala(id_sala), -- <<-- NOVA COLUNA
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);

CREATE TABLE IF NOT EXISTS Demanda (
    id_demanda SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    xp_recompensa INT NOT NULL,
    andar INT NOT NULL, 
    FOREIGN KEY (andar) REFERENCES Andar(id_andar),
    id_npc INT,
    FOREIGN KEY (id_npc) REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS DemandaConcluida (
    id_demanda INT NOT NULL,
    FOREIGN KEY (id_demanda) REFERENCES Demanda(id_demanda),
    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),
    data_conclusao TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id_demanda, id_estagiario)
);

CREATE TABLE IF NOT EXISTS Combate (
    id_combate SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),
    id_npc INT NOT NULL,
    FOREIGN KEY (id_npc) REFERENCES NPC(id_personagem),
    resultado VARCHAR(20) NOT NULL CHECK (resultado IN ('venceu', 'derrotado', 'fugiu')),
    data TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    dialogo_inicial TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Combate', 'Entrega', 'Conversa', 'Manutenção')),
    xp_recompensa INT NOT NULL,
    moedas_recompensa INT NOT NULL,
    npc_origem INT NOT NULL,
    FOREIGN KEY (npc_origem) REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS MissaoCombate (
    id_missao INT PRIMARY KEY,
    id_inimigo INT NOT NULL,
    quantidade_alvo INT NOT NULL,
    quantidade_atual INT DEFAULT 0,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);

CREATE TABLE IF NOT EXISTS MissaoConversa (
    id_missao INT PRIMARY KEY,
    id_npc_alvo INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_npc_alvo) REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS MissaoEntrega (
    id_missao INT PRIMARY KEY,
    id_item INT NOT NULL,
    quantidade INT NOT NULL,
    id_npc_destino INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_item) REFERENCES Item(id_item),
    FOREIGN KEY (id_npc_destino) REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS MissaoStatus (
    id_missao INT,
    id_estagiario INT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Disponível', 'Em Andamento', 'Concluída')),
    PRIMARY KEY (id_missao, id_estagiario),
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);

CREATE TABLE IF NOT EXISTS MissaoConcluida (
    id_missao INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),
    data_conclusao TIMESTAMP DEFAULT NOW(),
    xp_ganho INT NOT NULL DEFAULT 0,
    moedas_ganhas INT NOT NULL DEFAULT 0,
    PRIMARY KEY (id_missao, id_estagiario)
); 

CREATE OR REPLACE VIEW vw_posicao_estagiario AS
SELECT 
    e.id_personagem,
    e.andar_atual,
    e.sala_atual,
    a.numero as numero_andar,
    a.nome as nome_andar,
    s.nome as nome_sala,
    s.descricao as descricao_sala
FROM Estagiario e
JOIN Andar a ON e.andar_atual = a.id_andar
JOIN Sala s ON e.sala_atual = s.id_sala;

CREATE OR REPLACE VIEW vw_conexoes_salas AS
SELECT 
    cs.id_sala_origem,
    cs.id_sala_destino,
    s.nome as nome_sala_destino,
    s.id_andar as andar_destino,
    a.numero as numero_andar_destino
FROM ConexaoSala cs
JOIN Sala s ON cs.id_sala_destino = s.id_sala
JOIN Andar a ON s.id_andar = a.id_andar;

CREATE OR REPLACE VIEW vw_sala_central AS
SELECT 
    s.id_sala,
    s.id_andar,
    a.numero as numero_andar
FROM Sala s
JOIN Andar a ON s.id_andar = a.id_andar
WHERE s.nome = 'Sala Central';
