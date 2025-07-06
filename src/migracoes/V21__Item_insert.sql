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
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Mouse Gamer', 'Aumenta precisão permanentemente', 'Arma', 200),
('Teclado Mecânico', 'Aumenta velocidade de digitação', 'Arma', 300),
('Cadeira Ergonômica', 'Reduz dano recebido', 'Arma', 500),
('Livro básico de sql', 'ótimo contra bugs', 'Arma', 0);
