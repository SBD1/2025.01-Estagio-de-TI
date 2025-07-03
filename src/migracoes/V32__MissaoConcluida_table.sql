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