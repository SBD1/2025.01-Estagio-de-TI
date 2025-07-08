CREATE TABLE Dialogo (
    id_dialogo SERIAL PRIMARY KEY,
    id_npc INT,
    dialogo TEXT NOT NULL,
    FOREIGN KEY(id_npc) REFERENCES NPC(id_npc)
);