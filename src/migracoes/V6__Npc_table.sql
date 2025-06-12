CREATE TABLE IF NOT EXISTS NPC (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem),

    funcao VARCHAR(50) NOT NULL, -- Ex: 'Chefe', 'Colega', 'Contratante', 'Mercador', 'Usuário'
    andar INT REFERENCES Andar(id_andar)
);
