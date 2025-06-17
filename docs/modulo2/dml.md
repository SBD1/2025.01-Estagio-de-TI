# DML - Data Manipulation Language

A Linguagem de Manipulação de Dados (DML) é um conjunto de comandos SQL que permite a inserção, atualização, consulta e exclusão de dados em um banco de dados, populando a estrutura criada pela DDL.

-----

```sql
BEGIN TRANSACTION;

-- Inserção de dados com o prefixo do Schema para popular o mundo do jogo.

-- Inserções na tabela Andar
INSERT INTO SBD1.Andar (numero, descricao) VALUES
(1, 'Primeiro andar'),
(2, 'Segundo andar');

-- Inserções na tabela Sala
-- IDs são gerados sequencialmente (1 a 6)
INSERT INTO SBD1.Sala (id_andar, nome, descricao) VALUES
(1, 'Recepção', 'Você está na recepção. O ar cheira a café e papel antigo.'),
(1, 'Cafeteria', 'Um lugar para relaxar e tomar um café.'),
(1, 'Corredor 1A', 'Um corredor longo e silencioso no primeiro andar.'),
(2, 'Corredor 2A', 'Corredor do segundo andar. O carpete aqui é de um vermelho berrante.'),
(2, 'Escritório 201', 'Um escritório com uma grande janela de vidro.'),
(2, 'Sala de Reuniões', 'Uma sala imponente com uma mesa de mogno no centro.');

-- Inserções na tabela Conexao para ligar as salas
INSERT INTO SBD1.Conexao (id_sala_origem, id_sala_destino, nome_saida) VALUES
-- Saídas da Recepção (ID 1)
(1, 2, 'ir para a cafeteria'),
(1, 3, 'seguir pelo corredor'),
(1, 4, 'subir as escadas'), -- Conecta ao Corredor 2A (ID 4)

-- Saídas da Cafeteria (ID 2)
(2, 1, 'voltar para a recepção'),

-- Saídas do Corredor 1A (ID 3)
(3, 1, 'ir para a recepção'),

-- Saídas do Corredor 2A (ID 4)
(4, 5, 'entrar no escritório 201'),
(4, 6, 'ir para a sala de reuniões'),
(4, 1, 'descer as escadas'), -- Conecta à Recepção (ID 1)

-- Saídas do Escritório 201 (ID 5)
(5, 4, 'sair para o corredor'),

-- Saídas da Sala de Reuniões (ID 6)
(6, 4, 'sair para o corredor');


COMMIT;
```

\<center\>

## Histórico de Versão

| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: |
| `1.0`  | 17/06/2025 | Versão inicial do DML com dados de andares, salas e conexões. | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr) |

\</center\>