INSERT INTO Inimigo (id_inimigo, nome) VALUES
(1, 'Bug'),
(2, 'Malware'),
(3, 'Hacker');




INSERT INTO InstanciaInimigo (id_inimigo, vida, velocidade, id_pc) VALUES
(1, 100, 200, 1),
(1, 100, 200, 1),
(2, 500, 100, 2),
(2, 500, 100, 2),
(3, 900, 70, 3);

INSERT INTO Ataque (nome, dano, chance_acerto, efeito) VALUES
--PERSONAGEM
--todos
('Compilação Forçada', 25, 95, NULL),
('Debugger', 20, 100, 'lentidão'),
('Documentação Oficial', 15, 100, 'fraqueza'),
('Print de Rastreamento', 10, 100, 'azar'),
--para bugs
('Forçar Tipagem', 30, 90, 'fraqueza'),
('Refatoração Pesada', 35, 85, 'lentidão'),
('Console.log Massivo', 20, 100, 'fraqueza'),
--para malwares
('Antivírus Atualizado', 40, 80, 'lentidão'),
('Análise de Pacotes', 30, 90, 'azar'),
('Firewall Manual', 25, 95, 'fraqueza'),
--para hacker
('2FA Reforçado', 35, 90, 'fraqueza'),
('Reboot no Servidor', 45, 80, 'lentidão'),
('Senha Forte', 30, 100, NULL),
--bugs e hackers
('Validação de Entrada', 30, 100, 'fraqueza'),
('Teste Unitário', 25, 90, 'azar'),
--Hacker e malwares
('Atualização de Sistema', 40, 85, 'lentidão'),
('Limpeza de Cache', 30, 95, NULL),
--bugs e malwares
('Sistema Operacional Limpo', 35, 90, 'fraqueza'),
('Backup Restaurado', 45, 80, 'azar'),

--INIMIGOS
--bugs
('faltou ;', 10, 100, NULL),
('bug de schrodinger', 20, 50, 'fraqueza'),
('Variável Não Inicializada', 15, 95, 'fraqueza'),
('Loop Infinito', 25, 60, 'lentidão'),
('Erro de Segmentação', 35, 80, NULL),
('NULL Pointer', 20, 70, 'azar'),
--malware
('dogsniffing', 30, 100, NULL),
('Mineração de BitCoin', 40, 80, 'azar'),
('Trojan.exe', 50, 90, 'fraqueza'),
('Keylogger', 30, 100, NULL),
('Spyware Invisível', 20, 100, 'azar'),
('Ransomware', 70, 75, 'lentidão'),
--hackers
('Arquivo.bat', 50, 100, NULL),
('Ataque DDoS', 45, 85, 'lentidão'),
('Phishing', 25, 100, 'azar'),
('Exploração de Zero-Day', 60, 70, 'fraqueza'),
('Rootkit', 40, 95, NULL),
('Injeção SQL', 100, 90, 'lentidão');

--Relacionando ataques aos inimigos
INSERT INTO Inimigo_Ataque (id_inimigo, id_ataque) VALUES
--BUG
(1, 20), -- faltou ;
(1, 21), -- bug de schrodinger
(1, 22), -- Variável Não Inicializada
(1, 23), -- Loop Infinito
(1, 24), -- Erro de Segmentação
(1, 25), -- NULL Pointer
--MALWARE
(2, 26), -- dogsniffing
(2, 27), -- Mineração de BitCoin
(2, 28), -- Trojan.exe
(2, 29), -- Keylogger
(2, 30), -- Spyware Invisível
(2, 31), -- Ransomware
--HACKER
(3, 32), -- Arquivo.bat
(3, 33), -- Ataque DDoS
(3, 34), -- Phishing
(3, 35), -- Exploração de Zero-Day
(3, 36), -- Rootkit
(3, 37); -- Injeção SQL


