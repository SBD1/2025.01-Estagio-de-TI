
CREATE TABLE PersonagemAtaque (
    id_personagem INT NOT NULL,
    id_ataque INT NOT NULL,
    PRIMARY KEY (id_personagem, id_ataque),
    FOREIGN KEY (id_personagem) REFERENCES Estagiario(id_personagem),
    FOREIGN KEY (id_ataque) REFERENCES Ataque(id_ataque)
);