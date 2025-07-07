CREATE TABLE Batalha (
    id_batalha SERIAL PRIMARY KEY,
    id_personagem INT NOT NULL,
    id_pc INT NOT NULL,
    resultado TEXT CHECK (resultado in ('Vitória', 'Derrota', 'Fugiu')),
    FOREIGN KEY(id_personagem) REFERENCES Estagiario(id_personagem),
    FOREIGN KEY(id_pc) REFERENCES PC(id_pc)
);

CREATE TABLE BatalhaInimigos (
    id_batalha_inimigo SERIAL PRIMARY KEY,
    id_batalha INT NOT NULL,
    id_inimigo INT NOT NULL,
    FOREIGN KEY(id_inimigo) REFERENCES InstanciaInimigo(id_instancia),
    FOREIGN KEY(id_batalha) REFERENCES Batalha(id_batalha)

);

CREATE TABLE InstanciaEstagiario (
    id_instancia SERIAL PRIMARY KEY,
    id_personagem INT NOT NULL REFERENCES Estagiario(id_personagem),
    vida_atual INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Normal',
    duracao_status INT DEFAULT 0,
    id_batalha INT REFERENCES Batalha(id_batalha),
    criado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE Arma_Efeito_Inimigo (
    id_arma INT NOT NULL REFERENCES Item(id_item),
    id_inimigo INT NOT NULL REFERENCES Inimigo(id_inimigo),
    efeito_tipo VARCHAR(20) NOT NULL CHECK (efeito_tipo IN ('normal', 'efetivo', 'inefetivo')),
    PRIMARY KEY (id_arma, id_inimigo)
);

-- Frases aleatórias para ataques (para variar texto no jogo)
CREATE TABLE Frase_Ataque (
    id_frase SERIAL PRIMARY KEY,
    id_ataque INT NOT NULL REFERENCES Ataque(id_ataque),
    frase TEXT NOT NULL
);

