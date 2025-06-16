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