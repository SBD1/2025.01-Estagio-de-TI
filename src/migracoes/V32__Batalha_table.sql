CREATE TABLE Batalha (
    id_batalha SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL,
    id_pc INT NOT NULL,
    resultado TEXT NOT NULL CHECK (resultado in ('Vitória', 'Derrota')),
    FOREIGN KEY(id_estagiario) REFERENCES Estagiario(id_personagem),
    FOREIGN KEY(id_pc) REFERENCES PC(id_pc)
);

CREATE TABLE BatalhaInimigos (
    id_batalha_inimigo SERIAL PRIMARY KEY,
    id_batalha INT NOT NULL,
    id_inimigo INT NOT NULL,
    FOREIGN KEY(id_inimigo) REFERENCES InstanciaInimigo(id_instancia),
    FOREIGN KEY(id_batalha) REFERENCES Batalha(id_batalha)

);

-- Para efeitos de batalha do estagiario (como debuffs)
CREATE TABLE InstanciaEstagiario (
    id_instancia SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL REFERENCES Estagiario(id_personagem),
    vida INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Normal', -- exemplo: Normal, Confuso, lerdão...
    debuff_fraqueza BOOLEAN DEFAULT FALSE,
    debuff_lentidao BOOLEAN DEFAULT FALSE,
    debuff_azar BOOLEAN DEFAULT FALSE,
    id_batalha INT REFERENCES Batalha(id_batalha), -- se quiser ligar à batalha específica
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
