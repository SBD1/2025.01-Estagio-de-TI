--Inventario do personagem
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL UNIQUE,
    espaco_total INT NOT NULL DEFAULT 12, 
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);

CREATE TABLE ItemInventario (
    id_inventario INT NOT NULL,
    id_instancia INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_inventario, id_instancia),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (id_instancia) REFERENCES InstanciaItem(id_instancia)
);

CREATE TABLE ItemNoChao (
    id_instancia INT PRIMARY KEY REFERENCES InstanciaItem(id_instancia),
    id_sala INT NOT NULL,
    FOREIGN KEY (id_sala) REFERENCES Sala(id_sala)
);


CREATE TABLE ItemNpc (
    id_instancia INT PRIMARY KEY REFERENCES InstanciaItem(id_instancia),
    id_npc INT NOT NULL,
    FOREIGN KEY (id_npc) REFERENCES Npc(id_npc)
);
