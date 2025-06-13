CREATE TABLE IF NOT EXISTS ChefeFinal (
    id_personagem INT PRIMARY KEY,
    FOREIGN KEY (id_personagem) REFERENCES NPC(id_personagem),

    desafio_final VARCHAR(200) NOT NULL
);