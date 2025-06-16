CREATE TABLE IF NOT EXISTS NPC (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem),
    tipo VARCHAR(10) NOT NULL, -- Ex: 'Chefe', 'Colega', 'Almoxarife'
    andar_atual INT REFERENCES Andar(id_andar),
    dialogo_padrao VARCHAR(300) NOT NULL
);
