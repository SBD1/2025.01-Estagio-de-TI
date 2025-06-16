CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL UNIQUE,
    espaco_total INT NOT NULL DEFAULT 12, 
    espaco_usado INT NOT NULL DEFAULT 0,  
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);


CREATE TABLE IF NOT EXISTS ItemInventario (
    id_inventario INT,
    id_instancia INT,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_inventario, id_instancia),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (id_instancia) REFERENCES InstanciaItem(id_instancia)
);