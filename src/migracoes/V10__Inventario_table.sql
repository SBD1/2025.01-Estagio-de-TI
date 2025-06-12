CREATE TABLE IF NOT EXISTS Inventario (
    id_estagiario INT PRIMARY KEY,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
    -- A relação dos itens está em InstanciaItem (um inventário por estagiário)
);