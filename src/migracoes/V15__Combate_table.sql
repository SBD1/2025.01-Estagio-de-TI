CREATE TABLE IF NOT EXISTS Combate (
    id_combate SERIAL PRIMARY KEY,

    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),

    id_npc INT NOT NULL,
    FOREIGN KEY (id_npc) REFERENCES NPC(id_personagem),

    resultado VARCHAR(20) NOT NULL CHECK (resultado IN ('venceu', 'derrotado', 'fugiu')),
    data TIMESTAMP DEFAULT NOW()
);