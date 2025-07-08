INSERT INTO NPC (nome, tipo, sala_atual, dialogo_padrao, respeito_personagem) VALUES

--Colegas
('Severino', 'colega', 2, 'Os servidores precisam estar sempre funcionando...', 10),
('Maria', 'colega', 9, 'Olá estagiário! Como posso ajudar?', 10),
('Cláudio', 'colega', 3, 'Os servidores precisam estar sempre funcionando...', 10),
('Raimunda', 'colega', 20, 'Olá estagiário! Como posso ajudar?', 10),
('Cristiano', 'colega', 24, 'Os servidores precisam estar sempre funcionando...', 10),
('Ana', 'colega', 14, 'Olá estagiário! Como posso ajudar?', 10),

-- Almoxarife
('João', 'almoxarife', 5, 'Preciso organizar esse estoque...', 0),

-- Recepcionista
('Samara', 'recepcionista', 8, 'Olá estagiário, outros funcionários relataram um problema para você resolver.', 0),

-- Supervisores por andar (salas centrais de 10 a 37)
('Eduardo', 'supervisor', 10, 'Sou o responsável técnico deste andar. Precisa de ajuda com algo?', 10),
('Márcia', 'supervisor', 13, 'Sou a supervisora geral por aqui. Está tudo funcionando bem?', 20),
('José', 'supervisor', 16, 'Ei, você! Pode me ajudar com uma tarefa urgente?', 30),
('Luciana', 'supervisor', 19, 'Fique atento, temos muito trabalho a fazer neste andar.', 40),
('Paulo', 'supervisor', 22, 'Bem-vindo. Este andar é minha responsabilidade. Tudo certo por aqui?', 50),
('Tatiane', 'supervisor', 25, 'Olá, estagiário. Preciso que você realize algumas tarefas.', 60),
('Rogério', 'supervisor', 28, 'Problemas no setor? Me avise que cuidamos disso.', 70),
('Juliana', 'supervisor', 31, 'Este andar precisa de organização. Pode me ajudar?', 80),
('Fábio', 'supervisor', 34, 'Trabalho duro é o que faz este lugar girar. Está pronto?', 90),

-- Chefe
('Antônio', 'chefe', 37, 'Sou o chefe geral da empresa. Espero resultados do seu estágio.', 10);

INSERT INTO Dialogo(id_npc, dialogo) VALUES
(1, 'Os servidores precisam estar sempre funcionando. Já verificou o status deles hoje?'),
(2, 'Preciso organizar esse estoque... Se encontrar algum item perdido, me avise!'),
(3, 'Olá estagiário! Como posso ajudar?'),
(4, 'Os servidores precisam estar sempre funcionando. Já verificou o status deles hoje?'),
(5, 'Preciso organizar esse estoque... Se encontrar algum item perdido, me avise!'),
(6, 'Olá estagiário! Como posso ajudar?'),
(7, 'Os servidores precisam estar sempre funcionando. Já verificou o status deles hoje?'),
(8, 'Preciso organizar esse estoque... Se encontrar algum item perdido, me avise!'),
(9, 'Olá estagiário! Como posso ajudar?'),
(10, 'Olá estagiário, outros funcionários relataram um problema para você resolver. Os seguintes PCs estão com problemas: '),
-- Diálogos para Carlos (supervisor de TI, id_npc = 11)
(11, 'Falar sobre missões'),
(11, 'Ver missões disponíveis'),
(11, 'Sair'),
(11, 'Tenho missões técnicas para você! Preciso que elimine vírus e bugs dos nossos sistemas. Aceita a missão?'),
(11, 'Ótimo! Vá eliminar esses problemas nos PCs. Boa sorte!'),
(11, 'Sem problemas, volte quando estiver pronto.'),
-- Diálogos para Fernanda (supervisora administrativa, id_npc = 12)
(12, 'Falar sobre missões'),
(12, 'Ver missões disponíveis'),
(12, 'Sair'),
(12, 'Tenho missões administrativas para você! Preciso que converse com a equipe e entregue alguns itens. Aceita a missão?'),
(12, 'Perfeito! Vá fazer networking e entregar os itens. Sucesso!'),
(12, 'Tudo bem, volte quando quiser uma missão.');



