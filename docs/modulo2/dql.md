# DQL - Data Query Language

A DQL (Data Query Language) é uma sublinguagem do SQL focada em realizar consultas e recuperar dados de um banco de dados. Seus comandos permitem aos usuários e aplicações extrair informações específicas de tabelas, realizar junções e agregar dados para análise e relatórios.

### Consultas ao Banco de Dados

A seguir, estão listadas diversas consultas para interagir com o banco de dados do jogo.

-----

#### **1. Estrutura Física**

##### **1.1. Listar todos os mundos**

```sql
SELECT * FROM Mundo;
```

##### **1.2. Listar todos os andares de um mundo específico**

```sql
-- O valor '1' pode ser substituído pelo ID do mundo desejado.
SELECT * FROM Andar WHERE id_mundo = 1 ORDER BY numero;
```

##### **1.3. Listar todas as salas de um andar**

```sql
-- O valor '1' pode ser substituído pelo ID do andar desejado.
SELECT * FROM Sala WHERE id_andar = 1;
```

##### **1.4. Listar todas as cafeterias**

```sql
SELECT * FROM Cafeteria;
```

-----

#### **2. Personagens**

##### **2.1. Listar todos os personagens**

```sql
SELECT * FROM Personagem;
```

##### **2.2. Listar todos os estagiários**

```sql
SELECT * FROM Estagiario
JOIN Personagem ON Estagiario.id_personagem = Personagem.id_personagem;
```

##### **2.3. Listar todos os NPCs e suas funções**

```sql
SELECT NPC.*, Personagem.nome, Personagem.descricao
FROM NPC
JOIN Personagem ON NPC.id_personagem = Personagem.id_personagem;
```

##### **2.4. Listar todos os chefes finais**

```sql
SELECT ChefeFinal.*, Personagem.nome
FROM ChefeFinal
JOIN Personagem ON ChefeFinal.id_personagem = Personagem.id_personagem;
```

-----

#### **3. Itens e Inventário**

##### **3.1. Listar todos os itens**

```sql
SELECT * FROM Item;
```

##### **3.2. Listar todos os itens em uma sala específica**

```sql
-- O valor '4' pode ser substituído pelo ID da sala desejada.
SELECT InstanciaItem.*, Item.nome
FROM InstanciaItem
JOIN Item ON InstanciaItem.id_item = Item.id_item
WHERE id_sala = 4;
```

##### **3.3. Listar todos os itens no inventário de um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário desejado.
SELECT InstanciaItem.*, Item.nome
FROM InstanciaItem
JOIN Item ON InstanciaItem.id_item = Item.id_item
WHERE id_estagiario = 1;
```

##### **3.4. Listar inventários existentes**

```sql
SELECT * FROM Inventario;
```

-----

#### **4. Missões e Progresso**

##### **4.1. Listar todas as missões**

```sql
SELECT * FROM Missao;
```

##### **4.2. Listar missões de um andar específico**

```sql
-- O valor '1' pode ser substituído pelo número do andar.
SELECT Missao.* FROM Missao WHERE andar = 1;
```

##### **4.3. Listar missões concluídas por um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT MissaoConcluida.*, Missao.nome
FROM MissaoConcluida
JOIN Missao ON MissaoConcluida.id_missao = Missao.id_missao
WHERE id_estagiario = 1;
```

-----

#### **5. Demandas (Sidequests)**

##### **5.1. Listar todas as demandas**

```sql
SELECT * FROM Demanda;
```

##### **5.2. Listar demandas concluídas por estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT DemandaConcluida.*, Demanda.nome
FROM DemandaConcluida
JOIN Demanda ON DemandaConcluida.id_demanda = Demanda.id_demanda
WHERE id_estagiario = 1;
```

##### **5.3. Demandas abertas (não concluídas) para um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT D.*
FROM Demanda D
LEFT JOIN DemandaConcluida DC ON D.id_demanda = DC.id_demanda AND DC.id_estagiario = 1
WHERE DC.id_demanda IS NULL;
```

-----

#### **6. Interações e Eventos**

##### **6.1. Listar todos os diálogos de um personagem**

```sql
-- O valor '2' pode ser substituído pelo ID do personagem.
SELECT * FROM Dialogo WHERE id_personagem = 2;
```

##### **6.2. Listar todas as transações realizadas por um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT * FROM Transacao WHERE id_estagiario = 1;
```

##### **6.3. Listar todos os combates de um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT * FROM Combate WHERE id_estagiario = 1;
```

-----

#### **7. Consultas Avançadas e Relatórios**

##### **7.1. Quantidade de missões e demandas concluídas por estagiário**

```sql
SELECT
    P.nome,
    COUNT(DISTINCT MC.id_missao) AS missoes_concluidas,
    COUNT(DISTINCT DC.id_demanda) AS demandas_concluidas
FROM Personagem P
LEFT JOIN Estagiario E ON P.id_personagem = E.id_personagem
LEFT JOIN MissaoConcluida MC ON MC.id_estagiario = E.id_personagem
LEFT JOIN DemandaConcluida DC ON DC.id_estagiario = E.id_personagem
WHERE E.id_personagem IS NOT NULL
GROUP BY P.nome;
```

##### **7.2. Ranking de estagiários por XP**

```sql
SELECT P.nome, E.xp, E.nivel
FROM Estagiario E
JOIN Personagem P ON E.id_personagem = P.id_personagem
ORDER BY E.xp DESC, E.nivel DESC;
```

##### **7.3. Itens mais presentes nos inventários**

```sql
SELECT Item.nome, SUM(InstanciaItem.quantidade) AS total
FROM InstanciaItem
JOIN Item ON InstanciaItem.id_item = Item.id_item
GROUP BY Item.nome
ORDER BY total DESC;
```

##### **7.4. Missões e demandas pendentes de um estagiário**

```sql
-- O valor '1' pode ser substituído pelo ID do estagiário.
SELECT 'Missao' AS tipo, M.nome, M.descricao
FROM Missao M
LEFT JOIN MissaoConcluida MC ON M.id_missao = MC.id_missao AND MC.id_estagiario = 1
WHERE MC.id_missao IS NULL
UNION ALL
SELECT 'Demanda' AS tipo, D.nome, D.descricao
FROM Demanda D
LEFT JOIN DemandaConcluida DC ON D.id_demanda = DC.id_demanda AND DC.id_estagiario = 1
WHERE DC.id_demanda IS NULL;
```

\<br\>
\<center\>

## Histórico de Versão

| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: |
| `1.0`  | 17/06/2025 | Versão inicial do DQL com consultas para a estrutura do jogo de estágio. | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr) |

\</center\>