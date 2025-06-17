-- PowerUps
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Monitor Extra', 'Aumenta produtividade temporariamente', 'PowerUp', 100),
('Café Turbo', 'Energia extra por tempo limitado', 'PowerUp', 50),
('Fone Noise Cancelling', 'Aumenta foco temporariamente', 'PowerUp', 150);

INSERT INTO PowerUp (id_item, bonus_ataque, duracao) VALUES
(1, 20, 300),  
(2, 15, 180),  
(3, 10, 600);  

-- Consumíveis
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Água', 'Restaura um pouco de energia', 'Consumivel', 5),
('Café', 'Restaura energia', 'Consumivel', 10),
('Pão de Queijo', 'Restaura energia e foco', 'Consumivel', 15),
('Energético', 'Restaura muita energia', 'Consumivel', 25);

INSERT INTO Consumivel (id_item, recuperacao_vida) VALUES
(4, 10),
(5, 20),  
(6, 25),  
(7, 50);  

-- Equipamentos
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
('Mouse Gamer', 'Aumenta precisão permanentemente', 'Equipamento', 200),
('Teclado Mecânico', 'Aumenta velocidade de digitação', 'Equipamento', 300),
('Cadeira Ergonômica', 'Reduz dano recebido', 'Equipamento', 500);

INSERT INTO Equipamento (id_item, slot, bonus_permanente) VALUES
(8, 'Maos', 15),     
(9, 'Maos', 20),    
(10, 'Corpo', 30); 

INSERT INTO InstanciaItem (id_item, quantidade, local_atual) VALUES
(5, 10, 'Loja'),   
(6, 8, 'Loja'),    
(7, 5, 'Loja'),   
(4, 1, 'Chao'),  
(2, 1, 'Chao'),    
(8, 1, 'Inventario'),  
(5, 2, 'Inventario');  