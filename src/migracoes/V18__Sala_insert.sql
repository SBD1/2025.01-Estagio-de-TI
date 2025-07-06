INSERT INTO Sala (id_andar, nome, descricao) VALUES
-- Subsolo 2
(11, 'Sala Central', 'Uma sala gigantesca e gelada com servidores.'),           -- id_sala = 1
(11, 'Data Center', 'Fileiras de servidores zumbindo.'),                        -- id_sala = 2
(11, 'Sala de Controle', 'Monitores mostrando métricas dos servidores.'),      -- id_sala = 3

-- Subsolo 1
(12, 'Sala Central', 'Área principal do almoxarifado.'),                        -- id_sala = 4
(12, 'Depósito', 'Prateleiras com equipamentos.'),                              -- id_sala = 5
(12, 'Oficina', 'Bancadas para manutenção.'),                                   -- id_sala = 6

-- Térreo
(13, 'Sala Central', 'Área principal da recepção.'),                            -- id_sala = 7
(13, 'Recepção', 'Balcão com recepcionista.'),                                  -- id_sala = 8
(13, 'Área de Espera', 'Sofás e revistas tech.'),                               -- id_sala = 9

-- Andar 1
(1, 'Sala Central', 'Central do suporte básico.'),                              -- id_sala = 10
(1, 'Help Desk', 'Baias de atendimento.'),                                      -- id_sala = 11
(1, 'Sala de Treinamento', 'Sala com computadores em fileiras.'),              -- id_sala = 12

-- Andar 2
(2, 'Sala Central', 'Centro da oficina de hardware.'),                          -- id_sala = 13
(2, 'Laboratório', 'Bancadas com equipamentos.'),                               -- id_sala = 14
(2, 'Depósito de Peças', 'Estoque organizado.'),                                -- id_sala = 15

-- ANDAR 3
(3, 'Sala Central', 'Central de suporte remoto.'),                              -- id_sala = 16
(3, 'NOC', 'Sala de monitoramento.'),                                           -- id_sala = 17
(3, 'Sala de Atendimento', 'Estações de trabalho.'),                            -- id_sala = 18

-- ANDAR 4
(4, 'Sala Central', 'Centro de infraestrutura.'),                               -- id_sala = 19
(4, 'Sala de Servidores', 'Racks de equipamentos.'),                            -- id_sala = 20
(4, 'Sala de Redes', 'Central de cabeamento.'),                                 -- id_sala = 21

-- ANDAR 5
(5, 'Sala Central', 'Centro de operações de rede.'),                            -- id_sala = 22
(5, 'Sala de Monitoramento', 'Telões com métricas.'),                           -- id_sala = 23
(5, 'Laboratório de Redes', 'Área de testes.'),                                 -- id_sala = 24

-- ANDAR 6
(6, 'Sala Central', 'Centro de segurança.'),                                    -- id_sala = 25
(6, 'SOC', 'Centro de operações de segurança.'),                                -- id_sala = 26
(6, 'Sala de Testes', 'Ambiente isolado para testes.'),                         -- id_sala = 27

-- ANDAR 7
(7, 'Sala Central', 'Área de desenvolvimento web.'),                            -- id_sala = 28
(7, 'Frontend', 'Time de frontend.'),                                           -- id_sala = 29
(7, 'Design', 'Equipe de UX/UI.'),                                              -- id_sala = 30

-- ANDAR 8
(8, 'Sala Central', 'Área de backend.'),                                        -- id_sala = 31
(8, 'Desenvolvimento', 'Time de backend.'),                                     -- id_sala = 32
(8, 'Arquitetura', 'Planejamento de sistemas.'),                                -- id_sala = 33

-- ANDAR 9
(9, 'Sala Central', 'Centro de DevOps.'),                                       -- id_sala = 34
(9, 'CI/CD', 'Pipelines e automação.'),                                         -- id_sala = 35
(9, 'Containers', 'Orquestração e deploy.'),                                    -- id_sala = 36

-- ANDAR 10
(10, 'Sala Central', 'Recepção da diretoria.'),                                 -- id_sala = 37
(10, 'Sala do Chefe', 'Escritório principal.'),                                 -- id_sala = 38
(10, 'Sala de Reuniões', 'Mesa grande e tela de projeção.');                    -- id_sala = 39



INSERT INTO ConexaoSala (id_sala_origem, id_sala_destino) VALUES
--subsolo 2
(1, 2), 
(2, 1), 
(1, 3), 
(3, 1),
--subsolo 1 
(4, 5), 
(5, 4),
(4, 6), 
(6, 4), 
--térreo 
(7, 8),
(8, 7), 
(7, 9), 
(9, 7), 
--andar 1 
(10, 11), 
(11, 10), 
(10, 12), 
(12, 10), 
--andar 2 
(13, 14), 
(14, 13),
(13, 15), 
(15, 13), 
--andar 3 
(16, 17), 
(17, 16), 
(16, 18), 
(18, 16), 
--andar 4 
(19, 20),
(20, 19), 
(19, 21), 
(21, 19), 
--andar 5 
(22, 23),
(23, 22), 
(22, 24), 
(24, 22), 
--andar 6 
(25, 26),
(26, 25), 
(25, 27), 
(27, 25), 
--andar 7
(28, 29), 
(29, 28), 
(28, 30), 
(30, 28), 
--andar 8
(31, 32), 
(32, 31),
(31, 33), 
(33, 31), 
--andar 9
(34, 35), 
(35, 34), 
(34, 36), 
(36, 34), 
--andar 10 
(37, 38), 
(38, 37), 
(37, 39), 
(39, 37); 

INSERT INTO PC (id_pc, id_sala) VALUES
(1, 3),
(2, 1),
(3, 11),
(4, 12),
(5, 35),
(6, 32),
(7, 17),
(8, 38);