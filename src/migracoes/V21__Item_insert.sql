-- PowerUps
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Monitor Extra', 'Aumenta produtividade temporariamente', 'PowerUp', 100),
('Café Turbo', 'Energia extra por tempo limitado', 'PowerUp', 50),
('Fone Noise Cancelling', 'Aumenta foco temporariamente', 'PowerUp', 150);

-- Consumíveis
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Água', 'Restaura um pouco de energia', 'Consumivel', 5),
('Café', 'Restaura energia', 'Consumivel', 10),
('Pão de Queijo', 'Restaura energia e foco', 'Consumivel', 15),
('Energético', 'Restaura muita energia', 'Consumivel', 25);


-- Arma
INSERT INTO Item (nome, descricao, tipo, preco_base, nivel_minimo) VALUES
('Livro básico de sql', 'ótimo contra bugs', 'Arma', 0, 0),
('Livro Avançado de sql', 'Destruidor de bugs', 'Arma', 0, 0),
('Guia Definitivo de Depuração', 'Contém estratégias versáteis para todo tipo de ameaça.', 'Arma', 20, 3),
('Manual de Defesa Digital', 'Estratégias segmentadas para combater ameaças específicas.', 'Arma', 25, 4),
('Livro do senai', 'O ápice do conhecimento técnico em segurança digital.', 'Arma', 30, 5);

