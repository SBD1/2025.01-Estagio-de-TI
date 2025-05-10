BEGIN TRANSACTION;

-- Mundo
INSERT INTO Mundo (id_mundo, nome, data_inicio) VALUES
(1, 'Empresa Tech S/A', '2024-02-01') ON CONFLICT (id_mundo) DO NOTHING;

-- Andares
INSERT INTO Andar (id_andar, id_mundo, numero, nome, tema, descricao) VALUES
(-2, 1, -2, 'Subsolo 2', 'Sala dos Servidores', 'O frio e barulhento subsolo onde vivem os servidores da empresa.'),
(-1, 1, -1, 'Subsolo 1', 'Almoxarifado', 'Depósito de peças, cabos, ferramentas e drivers.'),
(0, 1, 0, 'Térreo', 'Recepção', 'O ponto de partida. Receba instruções e converse com NPCs.'),
(1, 1, 1, '1º Andar', 'Suporte Básico', 'Help Desk, reino das perguntas óbvias.'),
(2, 1, 2, '2º Andar', 'Problemas de Hardware', 'Necrotério dos PCs antigos.'),
(3, 1, 3, '3º Andar', 'Suporte Remoto', 'O Call Center dos Lamentos.'),
(4, 1, 4, '4º Andar', 'Infraestrutura', 'Labirinto dos Cabos Infinitos.'),
(5, 1, 5, '5º Andar', 'Servidores e Redes', 'Sala do Frio.'),
(6, 1, 6, '6º Andar', 'Segurança da Informação', 'Bunker da Cibersegurança.'),
(7, 1, 7, '7º Andar', 'Desenvolvimento Web', 'Reino do Stack Overflow.'),
(8, 1, 8, '8º Andar', 'Backend e Integrações', 'Masmorra do NullPointerException.'),
(9, 1, 9, '9º Andar', 'DevOps', 'Fortaleza dos Scripts Eternos.'),
(10, 1, 10, '10º Andar', 'Diretoria', 'A Sala do Chefe Supremo.') ON CONFLICT (id_andar) DO NOTHING;

-- Salas principais
INSERT INTO Sala (id_sala, id_andar, nome, descricao) VALUES
(1, -2, 'Data Center', 'Racks de servidores e ar-condicionado no máximo.'),
(2, -1, 'Almoxarifado Central', 'Prateleiras com cabos, peças e ferramentas.'),
(3, 0, 'Recepção', 'Balcão de entrada, onde tudo começa.'),
(4, 1, 'Help Desk', 'Estações de atendimento e filas de usuários.'),
(5, 2, 'Oficina de Manutenção', 'Mesas com PCs desmontados e peças espalhadas.'),
(6, 3, 'Central de Chamados', 'Telefones tocando e monitores com acesso remoto.'),
(7, 4, 'Sala de Cabeamento', 'Patch panels, racks e muitos cabos.'),
(8, 5, 'Sala do Servidor', 'Servidores piscando e ar gélido.'),
(9, 6, 'SOC', 'Centro de Segurança, cheio de telas e alertas.'),
(10, 7, 'Sala de Dev Web', 'Paredes cheias de post-its e quadros brancos.'),
(11, 8, 'Backoffice', 'Servidores de banco de dados e APIs.'),
(12, 9, 'Sala de DevOps', 'Scripts e pipelines em painéis.'),
(13, 10, 'Sala da Diretoria', 'Mesa de reunião imponente.') ON CONFLICT (id_sala) DO NOTHING;

-- Cafeteria
INSERT INTO Cafeteria (id_cafeteria, nome, aberto, descricao) VALUES
(1, 'Café do Estágio', TRUE, 'Oásis dos estagiários: café, salgados e energia.') ON CONFLICT (id_cafeteria) DO NOTHING;

-- Personagem principal
INSERT INTO Personagem (id_personagem, nome, tipo, descricao) VALUES
(1, 'João Estagiário', 'PC', 'Jovem sonhador em busca da efetivação.') ON CONFLICT (id_personagem) DO NOTHING;

INSERT INTO Estagiario (id_personagem, xp, nivel, coins, status, andar_atual) VALUES
(1, 0, 1, 10, 'Normal', 0) ON CONFLICT (id_personagem) DO NOTHING;

-- NPCs principais
INSERT INTO Personagem (id_personagem, nome, tipo, descricao) VALUES
(2, 'Sr. Silva', 'NPC', 'Chefe do RH, entrega a missão inicial.'),
(3, 'Dona Marlene', 'NPC', 'Recepcionista sempre atenta.'),
(4, 'Carlos Hardware', 'NPC', 'Veterano da manutenção de PCs.'),
(5, 'Usuário Perdido', 'NPC', 'Não sabe ligar o monitor.'),
(6, 'Chefe Supremo', 'NPC', 'Diretor da empresa, o desafio final.'),
(7, 'Barista', 'NPC', 'Atende na cafeteria e vende power-ups.'),
(8, 'Analista de Segurança', 'NPC', 'Responsável pelo bunker da cibersegurança.') ON CONFLICT (id_personagem) DO NOTHING;

INSERT INTO NPC (id_personagem, funcao, andar) VALUES
(2, 'Contratante', 0),
(3, 'Recepcionista', 0),
(4, 'Colega', 2),
(5, 'Usuário', 1),
(6, 'Chefe', 10),
(7, 'Mercador', NULL),
(8, 'Colega', 6) ON CONFLICT (id_personagem) DO NOTHING;

INSERT INTO ChefeFinal (id_personagem, desafio_final) VALUES
(6, 'Apresente um projeto sob pressão e resolva um incidente crítico.') ON CONFLICT (id_personagem) DO NOTHING;

-- Novos NPCs para demandas e ambientação
INSERT INTO Personagem (id_personagem, nome, tipo, descricao) VALUES
(9, 'Analista de Redes', 'NPC', 'Especialista em redes, sempre disposto a ajudar.'),
(10, 'Técnico Sênior', 'NPC', 'Veterano das manutenções complicadas.'),
(11, 'Usuário Curioso', 'NPC', 'Sempre faz perguntas sobre tecnologia.'),
(12, 'Instrutor Online', 'NPC', 'Oferece cursos e dicas rápidas.') ON CONFLICT (id_personagem) DO NOTHING;

INSERT INTO NPC (id_personagem, funcao, andar) VALUES
(9, 'Colega', 5),
(10, 'Colega', 2),
(11, 'Usuário', 3),
(12, 'Instrutor', 7) ON CONFLICT (id_personagem) DO NOTHING;

-- Itens principais e incrementados
INSERT INTO Item (id_item, nome, tipo, descricao, conhecimento_extra) VALUES
(1, 'Cabo de Rede', 'Hardware', 'Essencial para conectar computadores à rede.', NULL),
(2, 'Café Forte', 'PowerUp', 'Aumenta o foco e a energia temporariamente.', 'Foco'),
(3, 'Mouse Óptico', 'Hardware', 'Troca rápida para usuários apressados.', NULL),
(4, 'Manual de Impressora', 'Grimorio', 'Desbloqueia conhecimento para instalar impressoras.', 'Impressoras'),
(5, 'Salgadinho', 'Consumivel', 'Recupera energia.', NULL),
(6, 'Chave de Rack', 'Chave', 'Permite abrir o rack de servidores.', NULL),
(7, 'Notebook de Backup', 'Hardware', 'Usado para restaurar sistemas críticos.', NULL),
(8, 'Cartão de Acesso', 'Chave', 'Abre portas restritas do prédio.', NULL),
(9, 'Livro de Redes', 'Grimorio', 'Aprenda fundamentos de redes.', 'Redes'),
(10, 'Kit Ferramentas', 'Hardware', 'Kit com chaves e alicates.', 'Manutenção'),
(11, 'Curso Online: Segurança', 'Grimorio', 'Curso rápido de segurança da informação.', 'Segurança'),
(12, 'Energy Drink', 'PowerUp', 'Energia instantânea para virar a noite.', 'Foco'),
(13, 'Camiseta Geek', 'Consumivel', 'Aumenta seu carisma temporariamente.', 'Carisma'),
(14, 'Mousepad RGB', 'Consumivel', 'Te deixa mais rápido nas tarefas.', 'Velocidade'),
(15, 'Livro de SQL', 'Grimorio', 'Aprenda comandos SQL avançados.', 'Banco de Dados'),
(16, 'Fone de Ouvido', 'Consumivel', 'Ajuda a se concentrar em ambientes barulhentos.', 'Concentração') ON CONFLICT (id_item) DO NOTHING;

-- Instâncias de itens em salas e inventário
INSERT INTO InstanciaItem (id_instancia_item, id_item, id_sala, id_estagiario, quantidade) VALUES
(1, 1, 4, NULL, 2),
(2, 2, NULL, 1, 1),
(3, 3, 5, NULL, 1),
(4, 4, NULL, 1, 1),
(5, 5, 1, NULL, 3),
(6, 6, 8, NULL, 1),
(7, 7, NULL, NULL, 1),
(8, 8, 13, NULL, 1),
(9, 9, 8, NULL, 1),
(10, 10, 5, NULL, 2),
(11, 11, NULL, 1, 1),
(12, 12, 3, NULL, 2),
(13, 13, 4, NULL, 1),
(14, 14, 5, NULL, 1),
(15, 15, 11, NULL, 1),
(16, 16, 12, NULL, 1) ON CONFLICT (id_instancia_item) DO NOTHING;

-- Inventário inicial do estagiário
INSERT INTO Inventario (id_estagiario) VALUES
(1) ON CONFLICT (id_estagiario) DO NOTHING;

-- Missões principais
INSERT INTO Missao (id_missao, nome, descricao, xp_recompensa, andar) VALUES
(1, 'Primeiro Dia', 'Converse com a recepcionista e descubra sua primeira tarefa.', 10, 0),
(2, 'Troca de Cabo', 'Ajude um usuário a reconectar o PC à rede.', 20, 1),
(3, 'Arrume o Monitor', 'Ensine o usuário a ligar o monitor.', 15, 1),
(4, 'Conserte o PC Antigo', 'Troque peças e faça um PC antigo funcionar.', 25, 2),
(5, 'Atenda Chamados', 'Resolva três chamados remotos.', 30, 3),
(6, 'Organize o Rack', 'Deixe o cabeamento do rack impecável.', 35, 4),
(7, 'Configurar Servidor', 'Monte e configure um servidor local.', 40, 5),
(8, 'Remova Vírus', 'Limpe as estações infectadas.', 45, 6),
(9, 'Corrija o Site', 'Conserte bugs no site da empresa.', 50, 7),
(10, 'API Misteriosa', 'Integre uma API REST no sistema.', 55, 8),
(11, 'Script de Automação', 'Crie um script para automatizar tarefas repetitivas.', 60, 9),
(12, 'Desafio Final', 'Apresente o projeto e salve a empresa de um incidente crítico.', 100, 10) ON CONFLICT (id_missao) DO NOTHING;

INSERT INTO MissaoAndar (id_andar, id_missao) VALUES
(0, 1), (1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 10), (9, 11), (10, 12)
ON CONFLICT DO NOTHING;

INSERT INTO MissaoConcluida (id_missao, id_estagiario) VALUES
(1, 1) ON CONFLICT DO NOTHING;

-- Demandas (sidequests)
INSERT INTO Demanda (id_demanda, nome, descricao, xp_recompensa, andar, id_npc) VALUES
(1, 'Configurar Impressora Wi-Fi', 'Ajude um usuário a instalar uma impressora sem fio.', 15, 1, 5),
(2, 'Montar VLAN', 'Auxilie na configuração de uma VLAN para separar setores.', 25, 5, 9),
(3, 'Atualizar Inventário', 'Faça o levantamento dos equipamentos do almoxarifado.', 20, -1, 10),
(4, 'Tirar Dúvidas sobre Nuvem', 'Explique para o usuário curioso como funciona a computação em nuvem.', 10, 3, 11),
(5, 'Fazer Curso Online', 'Complete um curso online de segurança da informação.', 30, 7, 12),
(6, 'Organizar Estação de Trabalho', 'Deixe a estação de um colega mais ergonômica.', 10, 4, 4),
(7, 'Configurar Backup', 'Implemente um sistema de backup automático.', 22, 8, 9),
(8, 'Trocar Mousepad', 'Substitua o mousepad antigo por um novo RGB.', 5, 2, 10),
(9, 'Ajudar com Fone de Ouvido', 'Empreste um fone para um colega que precisa de concentração.', 7, 9, 12) ON CONFLICT (id_demanda) DO NOTHING;

INSERT INTO DemandaConcluida (id_demanda, id_estagiario) VALUES
(1, 1),
(4, 1) ON CONFLICT (id_demanda, id_estagiario) DO NOTHING;

-- Diálogos principais e incrementados
INSERT INTO Dialogo (id_dialogo, id_personagem, texto) VALUES
(1, 2, 'Bem-vindo, jovem! Sua jornada começa agora.'),
(2, 3, 'Por favor, preencha seu crachá na recepção.'),
(3, 5, 'Meu monitor não liga! Me ajuda, por favor!'),
(4, 4, 'Precisa de uma chave de fenda? Está no almoxarifado.'),
(5, 7, 'Um café para animar a semana? Só escolher o seu power-up!'),
(6, 6, 'Parabéns por chegar até aqui. Agora, vamos ver seu verdadeiro potencial.'),
(7, 9, 'Já leu sobre VLANs? Posso te passar um livro ótimo!'),
(8, 10, 'Nada como um bom kit de ferramentas, né?'),
(9, 11, 'O que é esse tal de "nuvem"?'),
(10, 12, 'Tem interesse em um curso rápido de segurança?') ON CONFLICT (id_dialogo) DO NOTHING;

-- Loja da Cafeteria com mais opções
INSERT INTO LojaCafeteria (id_loja, id_cafeteria, id_item, preco) VALUES
(1, 1, 2, 5),
(2, 1, 5, 3),
(3, 1, 12, 6),
(4, 1, 13, 8) ON CONFLICT (id_loja) DO NOTHING;

-- PowerUp e Consumível para novos itens
INSERT INTO PowerUp (id_item, buff, duracao) VALUES
(2, 'Foco+2, Energia+2', 3),
(12, 'Energia+3, Foco+1', 2) ON CONFLICT (id_item) DO NOTHING;

INSERT INTO Consumivel (id_item, efeito, quantidade) VALUES
(5, 'Recupera energia', 1),
(13, 'Carisma+2', 1),
(14, 'Velocidade+1', 1),
(16, 'Concentração+2', 1)
ON CONFLICT (id_item) DO NOTHING;

-- Chaves e Grimorios
INSERT INTO Chave (id_item, descricao_uso) VALUES
(6, 'Abre o rack de servidores.') ON CONFLICT (id_item) DO NOTHING;

INSERT INTO Grimorio (id_item, xp_necessario, habilidade) VALUES
(4, 10, 'Instalar impressoras com sucesso.'),
(9, 20, 'Compreender redes locais e VLANs.'),
(11, 30, 'Implementar políticas básicas de segurança.'),
(15, 25, 'Executar queries SQL avançadas.')
ON CONFLICT (id_item) DO NOTHING;

-- História incrementada
INSERT INTO Historia (id_item, texto) VALUES
(1, 'Seu primeiro dia começa com um frio na barriga e uma xícara de café. O prédio é imenso, e cada andar guarda um novo desafio.'),
(2, 'O chefe do RH te chama: "Estagiário, precisamos de você para uma missão importante!"'),
(3, 'No Help Desk, um usuário desesperado acena: "Meu monitor não liga!"'),
(4, 'Entre um chamado e outro, você descobre que o segredo do sucesso pode estar em um bom café.'),
(5, 'Finalmente, diante da diretoria, é hora de mostrar tudo que aprendeu e conquistar sua efetivação!'),
(6, 'Entre demandas e café, você percebe que cada desafio extra te prepara melhor para o topo.'),
(7, 'Ao ajudar colegas, descobre que o conhecimento compartilhado é o maior poder de um estagiário.'),
(8, 'O tempo passa, e seu crachá vai ganhando respeito nos corredores da empresa.')
ON CONFLICT (id_item) DO NOTHING;

COMMIT;

