CREATE TABLE IF NOT EXISTS Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('Hardware', 'Consumivel', 'Chave', 'Arma', 'Grimorio', 'Historia', 'PowerUp')),
    descricao VARCHAR(200) NOT NULL,
    conhecimento_extra VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Chave (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    descricao_uso VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Consumivel (
    id_item INT PRIMARY KEY,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),

    efeito VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade BETWEEN 1 AND 100)
);

CREATE TABLE IF NOT EXISTS PowerUp (
    id_item INT PRIMARY KEY,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),

    buff VARCHAR(100) NOT NULL,
    duracao INT NOT NULL -- em turnos ou minutos
);

CREATE TABLE IF NOT EXISTS Grimorio (
    id_item INT PRIMARY KEY,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),

    xp_necessario INT NOT NULL CHECK (xp_necessario BETWEEN 1 AND 10000),
    habilidade VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Historia (
    id_item INT PRIMARY KEY,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),

    texto VARCHAR(500) NOT NULL
);


CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia_item SERIAL PRIMARY KEY,

    id_item INT NOT NULL,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),

    id_sala INT,
    FOREIGN KEY (id_sala) REFERENCES Sala(id_sala),

    id_estagiario INT,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),

    quantidade INT NOT NULL DEFAULT 1
);