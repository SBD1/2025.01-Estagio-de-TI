CREATE TABLE IF NOT EXISTS Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    xp_recompensa INT NOT NULL,

    andar INT NOT NULL,
    FOREIGN KEY (andar) REFERENCES Andar(id_andar)
);

CREATE TABLE IF NOT EXISTS MissaoAndar (
    id_andar INT NOT NULL, 
    FOREIGN KEY (id_andar) REFERENCES Andar(id_andar),

    id_missao INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),

    PRIMARY KEY (id_andar, id_missao)
);

CREATE TABLE IF NOT EXISTS MissaoConcluida (
    id_missao INT NOT NULL,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),

    id_estagiario INT NOT NULL, 
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),

    data_conclusao TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id_missao, id_estagiario)
);
