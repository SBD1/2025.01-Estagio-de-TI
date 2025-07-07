-- 1. Estrutura do Mundo
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
-- Subsolo 2
(11, 'Sala Central', 'Uma sala gigantesca e gelada com servidores.'),
(11, 'Data Center', 'Fileiras de servidores zumbindo.'),
(11, 'Sala de Controle', 'Monitores mostrando métricas dos servidores.'),
-- Subsolo 1
(12, 'Sala Central', 'Área principal do almoxarifado.'),
(12, 'Depósito', 'Prateleiras com equipamentos.'),
(12, 'Oficina', 'Bancadas para manutenção.'),
-- Térreo
(13, 'Sala Central', 'Área principal da recepção.'),
(13, 'Recepção', 'Balcão com recepcionista.'),
(13, 'Área de Espera', 'Sofás e revistas tech.'),
(13, 'Cafeteria', 'O aroma de café fresco invade o ambiente.'),
-- Andares 1 a 10
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
(1, 2), (2, 1), (1, 3), (3, 1), (4, 5), (5, 4), (4, 6), (6, 4), (7, 8), (8, 7),
(7, 9), (9, 7), (7, 10), (10, 7), (11, 12), (12, 11), (11, 13), (13, 11), (14, 15),
(15, 14), (14, 16), (16, 14), (17, 18), (18, 17), (17, 19), (19, 17), (20, 21), (21, 20),
(20, 22), (22, 20), (23, 24), (24, 23), (23, 25), (25, 23), (26, 27), (27, 26), (26, 28),
(28, 26), (29, 30), (30, 29), (29, 31), (31, 29), (32, 33), (33, 32), (32, 34), (34, 32),
(35, 36), (36, 35), (35, 37), (37, 35), (38, 39), (39, 38), (38, 40), (40, 38);

-- 2. Personagens (Todos juntos)
INSERT INTO Personagem (nome, tipo, descricao) VALUES
('Severino', 'NPC', 'Responsável pelo Data Center'),
('João', 'NPC', 'Almoxarife dedicado'),
('Maria', 'NPC', 'Recepcionista prestativa'),
('Cláudio', 'NPC', 'Responsável pelo Data Center'),
('Pedro', 'NPC', 'Almoxarife dedicado'),
('Raimunda', 'NPC', 'Responsável pelo Data Center'),
('Cristiano', 'NPC', 'Almoxarife dedicado'),
('Manoel', 'NPC', 'Responsável pelo Data Center'),
('Ana', 'NPC', 'Almoxarife dedicado'),
('Breno', 'NPC', 'Barista simpático'),
('Carlos', 'NPC', 'Um dev de backend que vive à base de café e código.'),
('Sargento Silva', 'NPC', 'Chefe de segurança da informação, não tolera falhas.'),
('Fernanda', 'NPC', 'Analista de Suporte do 1º andar, sobrecarregada com tickets.'),
('Ricardo', 'NPC', 'Técnico de Hardware do 2º andar, um acumulador de peças.'),
('Laura', 'NPC', 'Operadora do NOC no 3º andar, mestra da paciência.'),
('Cliente Furioso', 'NPC', 'Um cliente temporário esperando na recepção, muito irritado.'),
('Otávio', 'NPC', 'Especialista em Infra do 4º andar, obcecado por organização de cabos.'),
('Vanessa', 'NPC', 'Engenheira de Redes do 5º andar, só fala em jargões.'),
('Daniel', 'NPC', 'Engenheiro DevOps do 9º andar, ama automação mais que tudo.'),
('Beatriz', 'NPC', 'Assistente executiva do 10º andar, o portão de entrada para o chefe.'),
('Dr. Everton "O Chefão"', 'NPC', 'O CEO da empresa. Sua palavra é a lei.');

-- 3. Itens (Definições base)
INSERT INTO Item (nome, descricao, tipo, preco_base) VALUES
-- PowerUps (IDs: 1-3)
('Monitor Extra', 'Aumenta produtividade temporariamente', 'PowerUp', 100),
('Café Turbo', 'Energia extra por tempo limitado', 'PowerUp', 50),
('Fone Noise Cancelling', 'Aumenta foco temporariamente', 'PowerUp', 150),
-- Consumíveis (IDs: 4-7)
('Água', 'Restaura um pouco de energia', 'Consumivel', 5),
('Café', 'Restaura energia', 'Consumivel', 10),
('Pão de Queijo', 'Restaura energia e foco', 'Consumivel', 15),
('Energético', 'Restaura muita energia', 'Consumivel', 25),
-- Equipamentos (IDs: 8-10)
('Mouse Gamer', 'Aumenta precisão permanentemente', 'Equipamento', 200),
('Teclado Mecânico', 'Aumenta velocidade de digitação', 'Equipamento', 300),
('Cadeira Ergonômica', 'Reduz dano recebido', 'Equipamento', 500),
-- Itens de Missão (IDs: 11-13)
('CD de Driver Antigo', 'Um CD raro para uma impressora fiscal pré-histórica.', 'Consumivel', 0),
('Capacitores Queimados', 'Um punhado de capacitores estufados, inúteis para a maioria, mas um tesouro para Ricardo.', 'Consumivel', 0),
('Script de Correção', 'Um script Python que promete consertar um pipeline de CI/CD quebrado.', 'Consumivel', 0);

-- 4. Itens Especializados (Detalhes)
INSERT INTO PowerUp (id_item, bonus_ataque, duracao) VALUES
(1, 20, 300),
(2, 15, 180),
(3, 10, 600);

INSERT INTO Consumivel (id_item, recuperacao_vida) VALUES
(4, 10),
(5, 20),
(6, 25),
(7, 50),
(11, 0), -- CD de Driver (sem recuperação de vida)
(12, 0), -- Capacitores (sem recuperação de vida)
(13, 0); -- Script (sem recuperação de vida)

INSERT INTO Equipamento (id_item, slot, bonus_ataque, bonus_defesa) VALUES
(8, 'Maos', 15, 0),
(9, 'Maos', 20, 0),
(10, 'Corpo', 0, 30);

-- 5. Instâncias de Itens (O que existe no mundo)
INSERT INTO InstanciaItem (id_item, quantidade, local_atual) VALUES
(5, 10, 'Loja'),
(6, 8, 'Loja'),
(7, 5, 'Loja'),
(4, 15, 'Loja'),
(8, 3, 'Loja'),
(9, 2, 'Loja'),
(10, 1, 'Loja'),
(4, 1, 'Chao'),
(2, 1, 'Chao'),
(8, 1, 'Inventario'),
(5, 2, 'Inventario');

-- 6. NPCs (Detalhes e localização)
INSERT INTO NPC (id_personagem, tipo, andar_atual, dialogo_padrao) VALUES
(1, 'colega', 11, 'Os servidores precisam estar sempre funcionando...'),
(2, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(3, 'colega', 13, 'Bem-vindo! Como posso ajudar?'),
(4, 'colega', 11, 'Os servidores precisam estar sempre funcionando...'),
(5, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(6, 'colega', 13, 'Bem-vindo! Como posso ajudar?'),
(7, 'colega', 7, 'Os servidores precisam estar sempre funcionando...'),
(8, 'almoxarife', 12, 'Preciso organizar esse estoque...'),
(9, 'colega', 7, 'Bem-vindo! Como posso ajudar?'),
(10, 'barista', 13, 'Bom dia! Que tal um cafezinho?'),
(11, 'colega', 8, 'Só mais um deploy e eu... ah, oi.'),
(12, 'chefe', 6, 'A segurança da informação é a prioridade máxima.'),
(13, 'colega', 1, 'Só mais um ticket... só mais um ticket... ah, olá. Precisa de algo?'),
(14, 'colega', 2, 'Não mexa nas minhas coisas! Cada capacitor, cada resistor tem seu lugar. Mais ou menos.'),
(15, 'colega', 3, 'Sim, senhor, já tentou reiniciar? Não, o computador, não o micro-ondas...'),
(16, 'cliente', 13, '(Ele está a andar de um lado para o outro, a bufar. Melhor não irritá-lo sem um bom motivo.)'),
(17, 'colega', 4, 'Veja esta simetria! Um cabo fora do lugar e todo o meu dia está arruinado.'),
(18, 'colega', 5, 'O throughput está ótimo, mas a latência no pacote ICMP para o DNS secundário está com jitter!'),
(19, 'colega', 9, 'Se é manual, está errado. Automatize tudo!'),
(20, 'assistente', 10, 'O Dr. Everton está numa reunião. Posso ajudar em algo?'),
(21, 'chefe', 10, 'Tempo é dinheiro. E você está a desperdiçar o meu.');

INSERT INTO ChefeFinal (id_personagem, desafio_final) VALUES
(21, 'Apresentação final do projeto de estágio para avaliação de efetivação.');

-- 7. Inimigos
INSERT INTO Inimigo (id_inimigo, nome, ataque) VALUES
(1, 'Bug', 'Ataque bizonho'),
(2, 'Malware', 'dogsniffing'),
(3, 'Hacker', 'Arquivo .bat'),
(4, 'Pacote Desgovernado', 'Inundação de Rede');

INSERT INTO InstanciaInimigo (id_inimigo, vida, dano) VALUES
(1, 100, 10), (1, 100, 10), (2, 500, 30), (2, 500, 30), (3, 900, 100), (4, 80, 20);

-- 8. Missões (Definições base)
INSERT INTO Missao (nome, descricao, dialogo_inicial, tipo, xp_recompensa, moedas_recompensa, npc_origem) VALUES
-- Missões Originais
('Vírus no Sistema', 'Elimine os vírus que estão infectando nossos servidores.', 'Socorro! Temos vários vírus nos servidores!', 'Combate', 100, 50, 1),
('Bugs em Produção', 'Mate os bugs que apareceram no sistema em produção.', 'O sistema está cheio de bugs! Pode eliminar eles?', 'Combate', 150, 70, 7),
('Network Inicial', 'Apresente-se aos funcionários do térreo.', 'Vamos conhecer o pessoal?', 'Conversa', 50, 20, 3),
('Conhecer a Equipe Dev', 'Converse com os desenvolvedores do 7º andar.', 'É importante conhecer o pessoal do desenvolvimento.', 'Conversa', 80, 40, 5),
('Café da Salvação', 'Entregue café para o dev que está há 3 dias sem dormir.', 'Preciso MUITO de café...', 'Entrega', 30, 20, 9),
('Hardware Novo', 'Leve estas peças novas para o pessoal do suporte.', 'Pode levar estas peças pro pessoal?', 'Entrega', 60, 40, 2),
('Check-up no Servidor', 'Verifique e reinicie o servidor que está superaquecendo no Data Center.', 'O Rack 03 está com a temperatura elevada! Por favor, vá até lá e reinicie o servidor para evitar um problema maior.', 'Manutenção', 75, 40, 1),
('O Ladrão de Pão de Queijo', 'Descubra quem está roubando os pães de queijo da cafeteria.', 'Não aguento mais! Alguém está pegando pães de queijo sem pagar. Me ajude a descobrir quem é!', 'Conversa', 120, 50, 10),
('Ataque na Rede!', 'Elimine os pacotes maliciosos que invadiram a rede após uma falha no firewall.', 'Invasores! Pacotes não identificados estão por toda parte. Contenha a ameaça!', 'Combate', 200, 100, 12),
-- Novas Missões
('O Fantasma da Impressora', 'Encontre o CD de driver para uma impressora antiga no almoxarifado para ajudar a Fernanda.', 'Pelo amor de tudo que é digital, não encontro o driver desta impressora em lugar nenhum!', 'Entrega', 120, 60, 13),
('Caça aos Capacitores', 'Colete 5 capacitores queimados de "Bugs" derrotados e entregue-os para Ricardo.', 'Estou a construir um... projeto secreto. Preciso de capacitores, mesmo os queimados. Consegue alguns para mim?', 'Entrega', 150, 75, 14),
('O Cliente Furioso', 'Vá até a recepção e converse com o cliente furioso para acalmá-lo antes que ele fale com a diretoria.', 'Temos um cliente nível "Vulcão em erupção" na recepção. Alguém precisa acalmá-lo. Você parece amigável.', 'Conversa', 100, 80, 15),
('O Pesadelo dos Cabos', 'Organize o rack de cabos na Sala de Redes para aliviar o TOC de Otávio.', 'Olhe para aquilo! Um emaranhado! Uma heresia! Por favor, arrume aquele rack antes que eu tenha um colapso.', 'Manutenção', 130, 70, 17),
('Latência Infernal', 'A rede está lenta. Vanessa suspeita de pacotes desgovernados. Elimine 3 deles.', 'Detetei uma anomalia! Latência altíssima! Suspeito de pacotes corrompidos a gerar colisões na camada 2. Elimine-os!', 'Combate', 180, 90, 18),
('Pipeline Quebrado', 'O pipeline de deploy quebrou. Pegue o script de correção com Daniel e entregue no Data Center.', 'O pipeline está vermelho! VERMELHO! Fiz este script de correção, mas preciso que alguém o leve até o Data Center no subsolo. Rápido!', 'Entrega', 250, 120, 19),
('O Projeto Final', 'Fale com Beatriz, a assistente do CEO, para iniciar seu desafio final pela efetivação.', 'Dr. Everton está pronto para o ver. Esta é a sua chance de provar o seu valor. Está preparado?', 'Conversa', 1000, 500, 20);

-- 9. Missões Especializadas (Detalhes)
INSERT INTO MissaoCombate (id_missao, id_inimigo, quantidade_alvo) VALUES
(1, 2, 1),  -- Vírus no Sistema
(2, 1, 5),  -- Bugs em Produção
(9, 4, 3),  -- Ataque na Rede!
(14, 4, 3); -- Latência Infernal

INSERT INTO MissaoConversa (id_missao, id_npc_alvo) VALUES
(3, 3),   -- Network Inicial
(4, 9),   -- Conhecer a Equipe Dev
(8, 11),  -- O Ladrão de Pão de Queijo
(12, 16), -- O Cliente Furioso
(16, 21); -- O Projeto Final

INSERT INTO MissaoEntrega (id_missao, id_item, quantidade, id_npc_destino) VALUES
(5, 5, 1, 9),   -- Café da Salvação
(6, 8, 3, 4),   -- Hardware Novo
(10, 11, 1, 13),-- O Fantasma da Impressora
(11, 12, 5, 14),-- Caça aos Capacitores
(15, 13, 1, 1); -- Pipeline Quebrado
