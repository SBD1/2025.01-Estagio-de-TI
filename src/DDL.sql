BEGIN TRANSACTION;

-- ==========================
-- 1. Mundo e Estrutura Física
-- ==========================
CREATE TABLE IF NOT EXISTS Mundo (
    id_mundo SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL DEFAULT 'Empresa Tech S/A',
    data_inicio DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Andar (
    id_andar SERIAL PRIMARY KEY,
    id_mundo INT NOT NULL REFERENCES Mundo(id_mundo),
    numero SMALLINT NOT NULL, -- -2 = Subsolo 2, -1 = Subsolo 1, 0 = Térreo, 1~10 = Andares
    nome VARCHAR(100) NOT NULL,
    tema VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Sala (
    id_sala SERIAL PRIMARY KEY,
    id_andar INT NOT NULL REFERENCES Andar(id_andar),
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Cafeteria (
    id_cafeteria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL DEFAULT 'Café do Estágio',
    aberto BOOLEAN NOT NULL DEFAULT TRUE,
    descricao TEXT
);

-- ==========================
-- 2. Personagens
-- ==========================
CREATE TABLE IF NOT EXISTS Personagem (
    id_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('PC', 'NPC')),
    descricao VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS Estagiario (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    xp INT NOT NULL CHECK (xp BETWEEN 0 AND 10000),
    nivel INT NOT NULL CHECK (nivel BETWEEN 1 AND 100),
    coins INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Normal', 'Confuso', 'Estressado', 'Motivado')),
    andar_atual INT NOT NULL REFERENCES Andar(id_andar)
);

CREATE TABLE IF NOT EXISTS NPC (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    funcao VARCHAR(50) NOT NULL, -- Ex: 'Chefe', 'Colega', 'Contratante', 'Mercador', 'Usuário'
    andar INT REFERENCES Andar(id_andar)
);

CREATE TABLE IF NOT EXISTS ChefeFinal (
    id_personagem INT PRIMARY KEY REFERENCES NPC(id_personagem),
    desafio_final VARCHAR(200) NOT NULL
);

-- ==========================
-- 3. Itens e Inventário
-- ==========================
CREATE TABLE IF NOT EXISTS Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('Hardware', 'Consumivel', 'Chave', 'Arma', 'Grimorio', 'Historia', 'PowerUp')),
    descricao VARCHAR(200) NOT NULL,
    conhecimento_extra VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia_item SERIAL PRIMARY KEY,
    id_item INT NOT NULL REFERENCES Item(id_item),
    id_sala INT REFERENCES Sala(id_sala),
    id_estagiario INT REFERENCES Estagiario(id_personagem),
    quantidade INT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Inventario (
    id_estagiario INT PRIMARY KEY REFERENCES Estagiario(id_personagem)
    -- A relação dos itens está em InstanciaItem (um inventário por estagiário)
);

-- ==========================
-- 4. Missões e Desafios
-- ==========================
CREATE TABLE IF NOT EXISTS Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    xp_recompensa INT NOT NULL,
    andar INT NOT NULL REFERENCES Andar(id_andar)
);

CREATE TABLE IF NOT EXISTS MissaoAndar (
    id_andar INT NOT NULL REFERENCES Andar(id_andar),
    id_missao INT NOT NULL REFERENCES Missao(id_missao),
    PRIMARY KEY (id_andar, id_missao)
);

CREATE TABLE IF NOT EXISTS MissaoConcluida (
    id_missao INT NOT NULL REFERENCES Missao(id_missao),
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    data_conclusao TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id_missao, id_estagiario)
);

-- ==========================
-- 5. Demandas (Sidequests)
-- ==========================
CREATE TABLE IF NOT EXISTS Demanda (
    id_demanda SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    xp_recompensa INT NOT NULL,
    andar INT NOT NULL REFERENCES Andar(id_andar),
    id_npc INT REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS DemandaConcluida (
    id_demanda INT NOT NULL REFERENCES Demanda(id_demanda),
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    data_conclusao TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id_demanda, id_estagiario)
);

-- ==========================
-- 6. Interações e Eventos
-- ==========================
CREATE TABLE IF NOT EXISTS Dialogo (
    id_dialogo SERIAL PRIMARY KEY,
    id_personagem INT NOT NULL REFERENCES Personagem(id_personagem),
    texto VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS Transacao (
    id_transacao SERIAL PRIMARY KEY,
    id_mercador INT NOT NULL REFERENCES NPC(id_personagem),
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    valor INT NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('venda', 'compra')),
    data TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Combate (
    id_combate SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    id_npc INT NOT NULL REFERENCES NPC(id_personagem),
    resultado VARCHAR(20) NOT NULL CHECK (resultado IN ('venceu', 'derrotado', 'fugiu')),
    data TIMESTAMP DEFAULT NOW()
);

-- ==========================
-- 7. Especializações de Itens
-- ==========================
CREATE TABLE IF NOT EXISTS Chave (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    descricao_uso VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Consumivel (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    efeito VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade BETWEEN 1 AND 100)
);

CREATE TABLE IF NOT EXISTS PowerUp (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    buff VARCHAR(100) NOT NULL,
    duracao INT NOT NULL -- em turnos ou minutos
);

CREATE TABLE IF NOT EXISTS Grimorio (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    xp_necessario INT NOT NULL CHECK (xp_necessario BETWEEN 1 AND 10000),
    habilidade VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Historia (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    texto VARCHAR(500) NOT NULL
);

-- ==========================
-- 8. Checkpoints e Progresso
-- ==========================
CREATE TABLE IF NOT EXISTS Checkpoint (
    id_checkpoint SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    id_sala INT NOT NULL REFERENCES Sala(id_sala),
    data TIMESTAMP DEFAULT NOW()
);

-- ==========================
-- 9. Conexões entre Salas
-- ==========================
CREATE TABLE IF NOT EXISTS ConexaoSala (
    id_conexao SERIAL PRIMARY KEY,
    id_sala_origem INT NOT NULL REFERENCES Sala(id_sala),
    id_sala_destino INT NOT NULL REFERENCES Sala(id_sala),
    direcao VARCHAR(10) NOT NULL CHECK (direcao IN ('Norte', 'Sul', 'Leste', 'Oeste')),
    descricao VARCHAR(200)
);

-- ==========================
-- 10. Loja da Cafeteria
-- ==========================
CREATE TABLE IF NOT EXISTS LojaCafeteria (
    id_loja SERIAL PRIMARY KEY,
    id_cafeteria INT NOT NULL REFERENCES Cafeteria(id_cafeteria),
    id_item INT NOT NULL REFERENCES Item(id_item),
    preco INT NOT NULL CHECK (preco >= 0)
);

COMMIT;
