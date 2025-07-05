CREATE TABLE Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE Ataque (
    id_ataque SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    dano INT NOT NULL,
    chance_acerto INT NOT NULL CHECK (chance_acerto >= 0 AND chance_acerto <= 100),
    efeito VARCHAR(100) CHECK(efeito IS NULL OR efeito IN ('fraqueza','lentidão', 'azar'))
);

-- tabela de relacao de inimigo e ataque
CREATE TABLE Inimigo_Ataque (
    id_inimigo INT REFERENCES Inimigo(id_inimigo),
    id_ataque INT REFERENCES Ataque(id_ataque),
    id_pc INT NOT NULL,
    PRIMARY KEY (id_inimigo, id_ataque),
    FOREIGN KEY(id_pc) REFERENCES PC(id_pc)
);

CREATE TABLE InstanciaInimigo (
    id_instancia SERIAL PRIMARY KEY,
    id_inimigo INT NOT NULL,
    vida int NOT NULL,
    velocidade int NOT NULL,
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);

