CREATE TABLE Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ataque VARCHAR(100) NOT NULL
);

CREATE TABLE InstanciaInimigo (
    id_instancia SERIAL PRIMARY KEY,
    id_inimigo INT NOT NULL,
    vida int NOT NULL,
    dano int NOT NULL,
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);