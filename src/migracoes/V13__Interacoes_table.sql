CREATE TABLE IF NOT EXISTS Dialogo (
    id_dialogo SERIAL PRIMARY KEY,

    id_personagem INT NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem),

    texto VARCHAR(500) NOT NULL
);
