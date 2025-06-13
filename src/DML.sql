-- Inserção de dados com o prefixo do Schema
INSERT INTO SBD1.Andar (numero, descricao) VALUES
(1, 'Primeiro andar'),
(2, 'Segundo andar');

INSERT INTO SBD1.Sala (id_andar, nome, descricao) VALUES
(1, 'Recepção', 'Você está na recepção. O ar cheira a café e papel antigo.'),
(1, 'Cafeteria', 'Um lugar para relaxar e tomar um café.'),
(1, 'Corredor 1A', 'Um corredor longo e silencioso no primeiro andar.'),
(2, 'Corredor 2A', 'Corredor do segundo andar. O carpete aqui é de um vermelho berrante.'),
(2, 'Escritório 201', 'Um escritório com uma grande janela de vidro.'),
(2, 'Sala de Reuniões', 'Uma sala imponente com uma mesa de mogno no centro.');

INSERT INTO SBD1.Conexao (id_sala_origem, id_sala_destino, nome_saida) VALUES
-- Recepção (ID 1)
(1, 2, 'ir para a cafeteria'),
(1, 3, 'seguir pelo corredor'),
(1, 4, 'subir as escadas'), -- Vai para o Corredor 2A

-- Cafeteria (ID 2)
(2, 1, 'voltar para a recepção'),

-- Corredor 1A (ID 3)
(3, 1, 'ir para a recepção'),

-- Corredor 2A (ID 4)
(4, 5, 'entrar no escritório 201'),
(4, 6, 'ir para a sala de reuniões'),
(4, 3, 'descer as escadas'), -- Vai para o Corredor 1A

-- Escritório 201 (ID 5)
(5, 4, 'sair para o corredor'),

-- Sala de Reuniões (ID 6)
(6, 4, 'sair para o corredor');