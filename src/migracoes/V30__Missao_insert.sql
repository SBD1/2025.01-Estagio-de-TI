-- Inserir missões na tabela Missao
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

('MalWares em todo canto',
 'Elimine os malwares dos computadores.',
 'Me ajude a acabar com os malwares dessa empresa',
 'Combate', 100, 50, 1),

('Hacker ingrato',
 'Um ex funcionário ingrato está hackeando a empresa.',
 'Ultimamente tem muitos hacker querendo acessar nossas informações valiosas, se você é o bonzão mesmo vai lá e destrói eles',
 'Combate', 150, 70, 7),

-- Missões de Conversa
('Network Inicial',
 'Apresente-se aos funcionários do térreo.',
 'Vamos conhecer o pessoal?',
 'Conversa', 50, 20, 3),

('Conhecer a Equipe Dev',
 'Converse com os desenvolvedores do 1º andar.',
 'É importante conhecer o pessoal do desenvolvimento, vai lá e arranja conversa com eles.',
 'Conversa', 80, 40, 5),

('Integração da Equipe',
 'Converse com todos os colegas para conhecer melhor a empresa.',
 'É importante que você conheça toda a equipe. Vá conversar com os colegas!',
 'Conversa', 100, 60, 12),

('Negociação pesada',
 'Negocie com o chefe sobre o possível aumento de salário.',
 'Estagiário, você poderia me ajudar rapidinho? Preciso que você vá até o chefe e peça um aumento de salário para mim, mas fale que é por mérito!',
 'Conversa', 100, 60, 12),

-- Missões de Entrega
('Café da Salvação',
 'Entregue café para o dev que está há 3 dias sem dormir.',
 'Preciso MUITO de café...',
 'Entrega', 30, 20, 9),

('Hardware Novo',
 'Leve estas peças novas para o pessoal do suporte.',
 'Pode levar estas peças pro pessoal?',
 'Entrega', 60, 40, 2);



-- Tabela de missões de combate
INSERT INTO MissaoCombate (id_missao, id_inimigo, quantidade_alvo) VALUES
(1, 2, 1), -- Matar 1 malware
(2, 1, 5), -- Matar 5 bugs
(3, 2, 3), -- Missão supervisor
(4, 3, 2); -- Missão supervisor

-- Tabela de missões de conversa
INSERT INTO MissaoConversa (id_missao, id_npc_alvo) VALUES
(5, 3),
(6, 9),
(7, 1),
(8, 3);


-- Tabela de missões de entrega
INSERT INTO MissaoEntrega (id_missao, id_item, quantidade, id_npc_destino) VALUES
(9, 1, 1, 5),
(10, 2, 3, 4);

