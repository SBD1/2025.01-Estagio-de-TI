INSERT INTO Inimigo (id_inimigo, nome) VALUES
(1, 'Bug'),
(2, 'Malware'),
(3, 'Hacker');

-- Primeiro vamos adicionar a coluna id_pc na InstanciaInimigo
ALTER TABLE InstanciaInimigo ADD COLUMN id_pc INT REFERENCES PC(id_pc);

INSERT INTO InstanciaInimigo (id_inimigo, vida, velocidade, id_pc) VALUES
(1, 100, 200, 1),
(1, 100, 200, 1),
(2, 500, 100, 2),
(2, 500, 100, 2),
(3, 900, 70, 3);

INSERT INTO Ataque (nome, dano, chance_acerto, efeito) VALUES
('faltou ;', 10, 100, NULL),
('bug de schrodinger', 20, 50, 'fraqueza'),
('dogsniffing', 30, 100, NULL),
('Mineração de BitCoin', 40, 80, 'azar'),
('Arquivo.bat', 50, 100, NULL),
('Injeção SQL', 100, 90, 'lentidão');

-- Relacionando ataques aos inimigos
INSERT INTO Inimigo_Ataque (id_inimigo, id_ataque, id_pc) VALUES
(1, 1, 1), (1, 2, 1),
(2, 3, 2), (2, 4, 2),
(3, 5, 3), (3, 6, 3);