-- Inserir diálogos para os NPCs

-- Diálogos para Severino (colega, id_npc = 1)
INSERT INTO Dialogo (id_npc, dialogo) VALUES 
(1, 'Oi! Como vai o trabalho?'),
(1, 'Perguntar sobre o trabalho'),
(1, 'Pedir ajuda'),
(1, 'Está tudo corrido por aqui. Os servidores vivem dando problema!'),
(1, 'Infelizmente não posso ajudar muito, mas boa sorte!');

-- Diálogos para João (almoxarife, id_npc = 2)
INSERT INTO Dialogo (id_npc, dialogo) VALUES 
(2, 'Precisa de algum equipamento?'),
(2, 'Ver equipamentos disponíveis'),
(2, 'Pedir ferramenta'),
(2, 'Temos cabos, teclados, mouses... o básico para manutenção.'),
(2, 'Pegue o que precisar, mas devolva depois!');

-- Diálogos para Maria (colega, id_npc = 3)
INSERT INTO Dialogo (id_npc, dialogo) VALUES 
(3, 'Olá estagiário! Como posso ajudar?'),
(3, 'Perguntar sobre o trabalho'),
(3, 'Pedir ajuda'),
(3, 'A recepção está sempre movimentada. Muitas pessoas com problemas!'),
(3, 'Posso te dar algumas dicas sobre como lidar com os usuários.');

-- Diálogos para Samara (recepcionista, id_npc = 10)
INSERT INTO Dialogo (id_npc, dialogo) VALUES
(10, 'Olá estagiário, outros funcionários relataram um problema para você resolver.');
