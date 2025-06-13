CREATE TABLE IF NOT EXISTS Transacao (
    id_transacao SERIAL PRIMARY KEY,

    id_mercador INT NOT NULL,
    FOREIGN KEY (id_mercador) REFERENCES NPC(id_personagem),

    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),

    valor INT NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('venda', 'compra')),
    data TIMESTAMP DEFAULT NOW()
);