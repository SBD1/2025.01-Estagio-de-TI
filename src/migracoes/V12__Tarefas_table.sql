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
