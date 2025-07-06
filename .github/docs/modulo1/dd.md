# DD - Dicionário de Dados

## Introdução

Um dicionário de dados é um recurso essencial na área da ciência de dados e da informática. Ele funciona como um catálogo ou compilação de informações sobre os dados utilizados em um sistema, banco de dados, projeto de pesquisa ou qualquer contexto em que a manipulação e interpretação de dados sejam necessárias.


## Entidade: Exemplo

**Descrição**: Esta entidade serve como um modelo para ilustrar como as informações são organizadas e descritas em um banco de dados. Inclui variáveis típicas, tipos de dados, valores permitidos e restrições.

**Observação**: Esta tabela é usada para exemplificar como preencher um dicionário de dados. Os valores e descrições são fictícios.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id-exemplo        | int        | Código de identificação do exemplo          | 1-1000            | PK, Not Null           |
| nome              | varchar(50)| Nome associado ao exemplo                   | a-z, A-Z          | Not Null               |
| data-criacao      | date       | Data em que o exemplo foi criado            | Data válida       | Not Null               |
| valor             | decimal(10,2)| Valor numérico do exemplo                 | 0.00-9999.99      | Not Null, Check (>= 0) |
| ativo             | boolean    | Indicador se o exemplo está ativo ou não    | True, False       | Not Null               |

  <font size="3"><p style="text-align: center"><b>Autores:</b> <a href="https://github.com/EmivaltoJrr">Emivalto da Costa Tavares Junior</a></font>

<details>
  <summary>Descrição de cada título da coluna</summary>

- "Nomes das variáveis": Identificadores específicos para cada conjunto de dados na tabela, como "id-exemplo" e "nome".<br>

- "Descrições das variáveis": Explicações sobre o que cada variável representa, como "Código de identificação do exemplo" e "Nome associado ao exemplo".<br>

- "Tipos de dados": Tipos de informações armazenadas, como inteiro, texto, data e decimal.<br>

- "Valores permitidos" : Intervalos ou opções permitidas para as variáveis, como "1-1000" para um identificador ou "True, False" para um indicador booleano.<br>

- "Restrições de Domínio": Inclui as restrições adicionais aplicáveis, como "PK" (chave primária), "Not Null" (não pode ser nulo), e "Check" (restrições de valor, como valores mínimos e máximos).

</details>


---

### Entidade: **Personagem**
**Descrição:** Representa os personagens do jogo.

| Nome Variável      | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|--------------------|-------|-------------------------------|--------------------|------------------------|
| id_personagem      | int   | Código de identificação do personagem | 1-1000            | PK, Not Null          |
| nome               | varchar | Nome do personagem            | 1-255 caracteres   | Not Null               |
| descrição          | text  | Descrição do personagem       | Livre              | Nullable               |

---

### Entidade: **Sala**
**Descrição:** Representa as salas disponíveis no jogo.

| Nome Variável      | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|--------------------|-------|-------------------------------|--------------------|------------------------|
| id_sala            | int   | Código de identificação da sala | 1-1000            | PK, Not Null          |
| nome               | varchar | Nome da sala                 | 1-255 caracteres   | Not Null               |
| descrição          | text  | Descrição da sala            | Livre              | Nullable               |

---

### Entidade: **Missão**
**Descrição:** Representa as missões que os jogadores podem realizar.

| Nome Variável      | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|--------------------|-------|-------------------------------|--------------------|------------------------|
| id_missao          | int   | Código de identificação da missão | 1-1000            | PK, Not Null          |
| nome               | varchar | Nome da missão               | 1-255 caracteres   | Not Null               |
| descrição          | text  | Descrição da missão          | Livre              | Nullable               |

---

### Entidade: **Tarefa**
**Descrição:** Representa as tarefas que compõem as missões.

| Nome Variável      | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|--------------------|-------|-------------------------------|--------------------|------------------------|
| id_tarefa          | int   | Código de identificação da tarefa | 1-1000            | PK, Not Null          |
| descrição          | text  | Descrição da tarefa          | Livre              | Nullable               |

---

### Entidade: **Item**
**Descrição:** Representa os itens disponíveis no jogo.

| Nome Variável      | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|--------------------|-------|-------------------------------|--------------------|------------------------|
| id_item            | int   | Código de identificação do item | 1-1000            | PK, Not Null          |
| nome               | varchar | Nome do item                 | 1-255 caracteres   | Not Null               |
| descrição          | text  | Descrição do item            | Livre              | Nullable               |
| preço              | float | Preço do item                | >= 0               | Nullable               |
| eh_unico           | bool  | Indica se o item é único     | true/false         | Default: false         |

---

### Entidade: **Instância Item**
**Descrição:** Representa instâncias específicas dos itens no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_instancia_item    | int   | Código de identificação da instância | 1-1000        | PK, Not Null          |
| id_item              | int   | Código de identificação do item | 1-1000            | FK, Not Null          |
| id_sala              | int   | Código de identificação da sala | 1-1000            | FK, Not Null          |

---

### Entidade: **Cafeteria**
**Descrição:** Representa a cafeteria do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_cafeteria         | int   | Código de identificação da cafeteria | 1-1000        | PK, Not Null          |
| itens_disponiveis    | text  | Lista de itens disponíveis    | Livre              | Nullable               |
| aberta               | bool  | Indica se a cafeteria está aberta | true/false     | Default: true          |

---

### Entidade: **Prédio**
**Descrição:** Representa os prédios do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_predio            | int   | Código de identificação do prédio | 1-1000          | PK, Not Null          |
| nome                 | varchar | Nome do prédio               | 1-255 caracteres   | Not Null               |

---

### Entidade: **Andar**
**Descrição:** Representa os andares dos prédios.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_andar             | int   | Código de identificação do andar | 1-1000           | PK, Not Null          |
| numero               | int   | Número do andar               | >= 0               | Not Null               |
| restrito             | bool  | Indica se o andar é restrito  | true/false         | Default: false         |

---

### Entidade: **Mundo**
**Descrição:** Representa o mundo do jogo, que contém diversos elementos como prédios e salas.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_mundo             | int   | Código de identificação do mundo | 1-1000          | PK, Not Null          |
| nome                 | varchar | Nome do mundo                | 1-255 caracteres   | Not Null               |
| descrição            | text  | Descrição do mundo            | Livre              | Nullable               |

---

### Entidade: **Colegas de Trabalho**
**Descrição:** Representa os colegas de trabalho no ambiente do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_colega            | int   | Código de identificação do colega | 1-1000          | PK, Not Null          |
| nome                 | varchar | Nome do colega               | 1-255 caracteres   | Not Null               |
| cargo                | varchar | Cargo do colega              | 1-255 caracteres   | Nullable               |

---

### Entidade: **Demanda**
**Descrição:** Representa demandas específicas que precisam ser atendidas no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_demanda           | int   | Código de identificação da demanda | 1-1000         | PK, Not Null          |
| descrição            | text  | Descrição da demanda          | Livre              | Nullable               |
| prioridade           | int   | Nível de prioridade da demanda | 1-5               | Default: 3            |

---

### Entidade: **Checkpoint**
**Descrição:** Representa pontos de salvamento ou progresso no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_checkpoint        | int   | Código de identificação do checkpoint | 1-1000      | PK, Not Null          |
| localização          | varchar | Localização do checkpoint    | 1-255 caracteres   | Not Null               |
| ativo                | bool  | Indica se o checkpoint está ativo | true/false     | Default: true          |

---

### Entidade: **Missão Contém**
**Descrição:** Representa a relação entre missões e tarefas.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_missao            | int   | Código de identificação da missão | 1-1000          | PK, FK, Not Null       |
| id_tarefa            | int   | Código de identificação da tarefa | 1-1000          | PK, FK, Not Null       |

---

### Entidade: **Consumíveis**
**Descrição:** Representa itens consumíveis disponíveis no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_consumivel        | int   | Código de identificação do consumível | 1-1000      | PK, Not Null          |
| nome                 | varchar | Nome do consumível           | 1-255 caracteres   | Not Null               |
| quantidade           | int   | Quantidade disponível         | >= 0               | Nullable               |

---

### Entidade: **Hardware**
**Descrição:** Representa equipamentos de hardware disponíveis no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_hardware          | int   | Código de identificação do hardware | 1-1000         | PK, Not Null          |
| nome                 | varchar | Nome do hardware             | 1-255 caracteres   | Not Null               |
| especificações       | text  | Detalhes técnicos do hardware | Livre              | Nullable               |

---

### Entidade: **Chefe**
**Descrição:** Representa os chefes ou inimigos principais do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_chefe             | int   | Código de identificação do chefe | 1-1000           | PK, Not Null          |
| nome                 | varchar | Nome do chefe                | 1-255 caracteres   | Not Null               |
| poder                | varchar | Poder ou habilidade especial | 1-255 caracteres   | Nullable               |

---

### Entidade: **Prédio Contém**
**Descrição:** Representa a relação entre prédios e seus andares.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_predio            | int   | Código de identificação do prédio | 1-1000          | PK, FK, Not Null       |
| id_andar             | int   | Código de identificação do andar | 1-1000           | PK, FK, Not Null       |

---

### Entidade: **Cafeteria Contém**
**Descrição:** Representa a relação entre a cafeteria e os itens disponíveis.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_cafeteria         | int   | Código de identificação da cafeteria | 1-1000        | PK, FK, Not Null       |
| id_item              | int   | Código de identificação do item | 1-1000            | PK, FK, Not Null       |

---

### Entidade: **Tarefa Envolve**
**Descrição:** Representa a relação entre tarefas e missões.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_tarefa            | int   | Código de identificação da tarefa | 1-1000          | PK, FK, Not Null       |
| id_missao            | int   | Código de identificação da missão | 1-1000          | PK, FK, Not Null       |

---

Vamos continuar detalhando as entidades restantes até concluirmos todas. 

---

### Entidade: **Jogador**
**Descrição:** Representa os jogadores do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_jogador           | int   | Código de identificação do jogador | 1-1000         | PK, Not Null          |
| nome                 | varchar | Nome do jogador              | 1-255 caracteres   | Not Null               |
| nível                | int   | Nível atual do jogador        | >= 0               | Default: 1            |
| experiência          | float | Experiência acumulada         | >= 0               | Default: 0            |

---

### Entidade: **Habilidades**
**Descrição:** Representa as habilidades que podem ser adquiridas ou utilizadas pelos jogadores.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_habilidade        | int   | Código de identificação da habilidade | 1-1000      | PK, Not Null          |
| nome                 | varchar | Nome da habilidade           | 1-255 caracteres   | Not Null               |
| descrição            | text  | Descrição da habilidade       | Livre              | Nullable               |
| custo                | float | Custo para adquirir ou usar a habilidade | >= 0       | Nullable               |

---

### Entidade: **Inventário**
**Descrição:** Representa o inventário dos jogadores, contendo os itens que possuem.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_inventario        | int   | Código de identificação do inventário | 1-1000        | PK, Not Null          |
| id_jogador           | int   | Código de identificação do jogador | 1-1000         | FK, Not Null          |
| id_item              | int   | Código de identificação do item | 1-1000            | FK, Not Null          |
| quantidade           | int   | Quantidade do item no inventário | >= 0             | Default: 0            |

---

### Entidade: **NPC**
**Descrição:** Representa os NPCs (personagens não jogáveis) do jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_npc               | int   | Código de identificação do NPC | 1-1000            | PK, Not Null          |
| nome                 | varchar | Nome do NPC                  | 1-255 caracteres   | Not Null               |
| função               | varchar | Função ou papel do NPC        | 1-255 caracteres   | Nullable               |
| diálogo              | text  | Diálogo padrão do NPC         | Livre              | Nullable               |

---

### Entidade: **Recompensa**
**Descrição:** Representa as recompensas que os jogadores podem receber ao completar missões ou tarefas.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_recompensa        | int   | Código de identificação da recompensa | 1-1000        | PK, Not Null          |
| tipo                 | varchar | Tipo da recompensa           | "item", "moeda", "experiência" | Not Null |
| valor                | float | Valor da recompensa           | >= 0               | Nullable               |

---

### Entidade: **Moeda**
**Descrição:** Representa a moeda do jogo utilizada para transações.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_moeda             | int   | Código de identificação da moeda | 1-1000           | PK, Not Null          |
| nome                 | varchar | Nome da moeda                | 1-255 caracteres   | Not Null               |
| valor_base           | float | Valor base da moeda           | >= 0               | Default: 1            |

---

### Entidade: **Quests**
**Descrição:** Representa as quests que os jogadores podem realizar, que podem ser compostas por múltiplas missões.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_quest             | int   | Código de identificação da quest | 1-1000           | PK, Not Null          |
| nome                 | varchar | Nome da quest                | 1-255 caracteres   | Not Null               |
| descrição            | text  | Descrição da quest            | Livre              | Nullable               |

---

### Entidade: **Jogador Completa**
**Descrição:** Representa a relação entre jogadores e missões ou quests que completaram.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_jogador           | int   | Código de identificação do jogador | 1-1000         | PK, FK, Not Null       |
| id_quest             | int   | Código de identificação da quest | 1-1000           | PK, FK, Nullable       |
| id_missao            | int   | Código de identificação da missão | 1-1000          | PK, FK, Nullable       |
| data_conclusao       | date  | Data de conclusão             | YYYY-MM-DD         | Nullable               |

---

### Entidade: **Log de Eventos**
**Descrição:** Representa o registro de eventos que ocorrem no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_evento            | int   | Código de identificação do evento | 1-1000          | PK, Not Null          |
| id_jogador           | int   | Código de identificação do jogador | 1-1000         | FK, Nullable           |
| tipo_evento          | varchar | Tipo de evento               | "missão", "compra", "batalha", etc. | Not Null |
| descrição            | text  | Descrição do evento           | Livre              | Nullable               |
| data_hora            | datetime | Data e hora do evento        | YYYY-MM-DD HH:MM:SS | Not Null               |

---

### Entidade: **Batalhas**
**Descrição:** Representa as batalhas que ocorrem no jogo.

| Nome Variável        | Tipo  | Descrição                     | Valores Permitidos | Restrições de Domínio |
|----------------------|-------|-------------------------------|--------------------|------------------------|
| id_batalha           | int   | Código de identificação da batalha | 1-1000         | PK, Not Null          |
| id_jogador           | int   | Código de identificação do jogador | 1-1000         | FK, Not Null           |
| id_chefe             | int   | Código de identificação do chefe | 1-1000           | FK, Not Null           |
| resultado            | varchar | Resultado da batalha         | "vitória", "derrota" | Not Null              |
| data_hora            | datetime | Data e hora da batalha       | YYYY-MM-DD HH:MM:SS | Not Null               |

---



## Histórico de Versão

| Versão | Data | Descrição | Autor(es) | Revisor |
| :-: | :-: | :-: | :-: | :-: |
| `1.0`  | 02/05/2025 | Primeira versão  do MER  | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr)  | [Gabriel Basto Bertolazi](https://github.com/Bertolazi) |
| `1.1`  | 02/05/2025 | adição de intem do DD  | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr)  |  |
