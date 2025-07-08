CREATE TABLE DropInimigo (
    id_inimigo INT REFERENCES Inimigo(id_inimigo),
    id_item INT REFERENCES Item(id_item),
    chance_drop REAL CHECK (chance_drop BETWEEN 0 AND 1),
    PRIMARY KEY (id_inimigo, id_item)
);

CREATE TABLE DropMissao (
    id_missao INT REFERENCES Missao(id_missao),
    id_item INT REFERENCES Item(id_item),
    chance_drop REAL CHECK (chance_drop BETWEEN 0 AND 1),
    PRIMARY KEY (id_missao, id_item)
);
