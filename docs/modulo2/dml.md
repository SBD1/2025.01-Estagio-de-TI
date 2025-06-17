# DML - Data Manipulation Language

## Introdução

A Linguagem de Manipulação de Dados (DML) é um conjunto de comandos SQL que permite a inserção, atualização, consulta e exclusão de dados em um banco de dados, populando a estrutura criada pela DDL.

## Migrações do Banco de Dados

### V16__Mundo_insert.sql
```sql
INSERT INTO Mundo (nome, descricao) VALUES
('Empresa TechStyle', 'Uma empresa de tecnologia moderna com vários andares');
```

### V17__Andar_insert.sql
```sql
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
```


### V20__Personagens_insert.sql
```sql
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
```
### V21__Item_insert.sql
```sql
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
```
### V27__Npc_insert.sql
```sql
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
```

### V29__Inimigo_insert.sql
```sql
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
```

### V30__Missao_insert.sql
```sql
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
```
## Histórico de Versão

| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: |
| `1.0`  | 16/06/2025 | Versão inicial do DML com dados de andares, salas e conexões. | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr) e [Lucas Mendonça Arruda](https://github.com/lucasarruda9) |
