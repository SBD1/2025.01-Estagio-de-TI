CREATE TABLE IF NOT EXISTS NPC (
    id_npc SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- Ex: 'Chefe', 'Colega', 'Almoxarife'
    sala_atual INT REFERENCES Sala(id_sala),
    dialogo_padrao VARCHAR(300) NOT NULL,
    respeito_personagem INT NOT NULL

);
