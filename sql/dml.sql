INSERT INTO Mundo (id_mundo, nome, data_inicio) VALUES
(1, 'Mundo dos estagiários', CURRENT_DATE);

INSERT INTO Andar(id_andar, id_mundo, numero, nome) VALUES
(11, 1, -2, 'Subsolo 2: Data Center'),
(12, 1, -1, 'Subsolo 1: Almoxarifado'),
(13, 1, 0, 'Térreo: Recepção'),
(1, 1, 1, 'Andar 1: Suporte Básico'),
(2, 1, 2, 'Andar 2: Problemas de Hardware'),
(3, 1, 3, 'Andar 3: Suporte Remoto'),
(4, 1, 4, 'Andar 4: Infraestrutura'),
(5, 1, 5, 'Andar 5: Redes'),
(6, 1, 6, 'Andar 6: Segurança'),
(7, 1, 7, 'Andar 7: Desenvolvimento Web'),
(8, 1, 8, 'Andar 8: Backend'),
(9, 1, 9, 'Andar 9: DevOps'),
(10, 1, 10, 'Andar 10: Diretoria');

INSERT INTO Sala (id_andar, nome, descricao) VALUES
(11, 'Sala Central', 'Uma sala gigantesca e gelada com servidores.'),
(11, 'Data Center', 'Fileiras de servidores zumbindo.'),
(11, 'Sala de Controle', 'Monitores mostrando métricas dos servidores.'),
(12, 'Sala Central', 'Área principal do almoxarifado.'),
(12, 'Depósito', 'Prateleiras com equipamentos.'),
(12, 'Oficina', 'Bancadas para manutenção.'),
(13, 'Sala Central', 'Área principal da recepção.'),
(13, 'Recepção', 'Balcão com recepcionista.'),
(13, 'Área de Espera', 'Sofás e revistas tech.'),
(1, 'Sala Central', 'Central do suporte básico.'),
(1, 'Help Desk', 'Baias de atendimento.'),
(1, 'Sala de Treinamento', 'Sala com computadores em fileiras.'),
(2, 'Sala Central', 'Centro da oficina de hardware.'),
(2, 'Laboratório', 'Bancadas com equipamentos.'),
(2, 'Depósito de Peças', 'Estoque organizado.'),
(3, 'Sala Central', 'Central de suporte remoto.'),
(3, 'NOC', 'Sala de monitoramento.'),
(3, 'Sala de Atendimento', 'Estações de trabalho.'),
(4, 'Sala Central', 'Centro de infraestrutura.'),
(4, 'Sala de Servidores', 'Racks de equipamentos.'),
(4, 'Sala de Redes', 'Central de cabeamento.'),
(5, 'Sala Central', 'Centro de operações de rede.'),
(5, 'Sala de Monitoramento', 'Telões com métricas.'),
(5, 'Laboratório de Redes', 'Área de testes.'),
(6, 'Sala Central', 'Centro de segurança.'),
(6, 'SOC', 'Centro de operações de segurança.'),
(6, 'Sala de Testes', 'Ambiente isolado para testes.'),
(7, 'Sala Central', 'Área de desenvolvimento web.'),
(7, 'Frontend', 'Time de frontend.'),
(7, 'Design', 'Equipe de UX/UI.'),
(8, 'Sala Central', 'Área de backend.'),
(8, 'Desenvolvimento', 'Time de backend.'),
(8, 'Arquitetura', 'Planejamento de sistemas.'),
(9, 'Sala Central', 'Centro de DevOps.'),
(9, 'CI/CD', 'Pipelines e automação.'),
(9, 'Containers', 'Orquestração e deploy.'),
(10, 'Sala Central', 'Recepção da diretoria.'),
(10, 'Sala do Chefe', 'Escritório principal.'),
(10, 'Sala de Reuniões', 'Mesa grande e tela de projeção.');


INSERT INTO ConexaoSala (id_sala_origem, id_sala_destino) VALUES
-- Subsolo 2
(1, 2), 
(2, 1), 
(1, 3), 
(3, 1),
-- Subsolo 1 
(4, 5), 
(5, 4),
(4, 6), 
(6, 4), 
-- Térreo 
(7, 8),
(8, 7), 
(7, 9), 
(9, 7), 
-- Andar 1 
(10, 11), 
(11, 10), 
(10, 12), 
(12, 10), 
-- Andar 2 
(13, 14), 
(14, 13),
(13, 15), 
(15, 13), 
-- Andar 3 
(16, 17), 
(17, 16), 
(16, 18), 
(18, 16), 
-- Andar 4 
(19, 20),
(20, 19), 
(19, 21), 
(21, 19), 
-- Andar 5 
(22, 23),
(23, 22), 
(22, 24), 
(24, 22), 
-- Andar 6 
(25, 26),
(26, 25), 
(25, 27), 
(27, 25), 
-- Andar 7
(28, 29), 
(29, 28), 
(28, 30), 
(30, 28), 
-- Andar 8
(31, 32), 
(32, 31),
(31, 33), 
(33, 31), 
-- Andar 9
(34, 35), 
(35, 34), 
(34, 36), 
(36, 34), 
-- Andar 10 
(37, 38), 
(38, 37), 
(37, 39), 
(39, 37); 




INSERT INTO Personagem (nome, tipo, descricao) VALUES
('Severino', 'NPC', 'Responsável pelo Data Center'),
('João', 'NPC', 'Almoxarife dedicado'),
('Maria', 'NPC', 'Recepcionista prestativa'),
('Cláudio', 'NPC', 'Responsável pelo Data Center'),
('Pedro', 'NPC', 'Almoxarife dedicado'),
('Raimunda', 'NPC', 'Responsável pelo Data Center'),
('Cristiano', 'NPC', 'Almoxarife dedicado'),
('Manoel', 'NPC', 'Responsável pelo Data Center'),
('Ana', 'NPC', 'Almoxarife dedicado');

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



INSERT INTO NPC (id_personagem, tipo, andar_atual, dialogo_padrao) VALUES
(1, 'colega', 11, 'Os servidores precisam estar sempre funcionando...'),
(2, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(3, 'colega', 13, 'Bem-vindo! Como posso ajudar?'),
(4, 'colega', 11, 'Os servidores precisam estar sempre funcionando...'),
(5, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(6, 'colega', 13, 'Bem-vindo! Como posso ajudar?'),
(7, 'colega', 11, 'Os servidores precisam estar sempre funcionando...'),
(8, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(9, 'colega', 13, 'Bem-vindo! Como posso ajudar?');

INSERT INTO Inimigo (id_inimigo, nome, ataque) VALUES
(1, 'Bug', 'Ataque bizonho'),
(2, 'Malware', 'dogsniffing'),
(3, 'Hacker', 'Arquivo .bat');

INSERT INTO InstanciaInimigo (id_inimigo, vida, dano) VALUES
(1, 100, 10),
(1, 100, 10),
(2, 500, 30),
(2, 500, 30),
(3, 900, 100);

INSERT INTO Missao (nome, descricao, dialogo_inicial, tipo, xp_recompensa, moedas_recompensa, npc_origem) VALUES
-- Missões de Combate
('Vírus no Sistema', 
 'Elimine os vírus que estão infectando nossos servidores.',
 'Socorro! Temos vários vírus nos servidores!',
 'Combate', 100, 50, 1),

('Bugs em Produção',
 'Mate os bugs que apareceram no sistema em produção.',
 'O sistema está cheio de bugs! Pode eliminar eles?',
 'Combate', 150, 70, 7),

-- Missões de Conversa
('Network Inicial',
 'Apresente-se aos funcionários do térreo.',
 'Vamos conhecer o pessoal?',
 'Conversa', 50, 20, 3),

('Conhecer a Equipe Dev',
 'Converse com os desenvolvedores do 7º andar.',
 'É importante conhecer o pessoal do desenvolvimento.',
 'Conversa', 80, 40, 5),

-- Missões de Entrega
('Café da Salvação',
 'Entregue café para o dev que está há 3 dias sem dormir.',
 'Preciso MUITO de café...',
 'Entrega', 30, 20, 9),

('Hardware Novo',
 'Leve estas peças novas para o pessoal do suporte.',
 'Pode levar estas peças pro pessoal?',
 'Entrega', 60, 40, 2);

-- Depois especifica os detalhes de cada tipo de missão
INSERT INTO MissaoCombate (id_missao, id_inimigo, quantidade_alvo) VALUES
(1, 2, 1), -- Matar 3 vírus
(2, 1, 5); -- Matar 5 bugs

INSERT INTO MissaoConversa (id_missao, id_npc_alvo) VALUES
(3, 3), -- Falar com a recepcionista
(4, 9); -- Falar com o dev frontend

INSERT INTO MissaoEntrega (id_missao, id_item, quantidade, id_npc_destino) VALUES
(5, 1, 1, 5), -- Entregar 1 café para o dev
(6, 2, 3, 4);  -- Entregar 3 peças para o suporte

