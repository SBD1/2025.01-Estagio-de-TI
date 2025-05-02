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

### Entidade: Personagem

**Descrição**: Representa os personagens no jogo, podendo ser jogadores (PC) ou não jogadores (NPC).

**Observação**: Esta tabela não possui chave estrangeira.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_personagem     | int        | Código de identificação do personagem      | 1-1000             | PK, Not Null           |
| nome              | varchar(50)| Nome associado ao personagem               | a-z, A-Z           | Not Null               |
| descricao         | varchar(50)| Descrição do personagem                    | a-z, A-Z           | Not Null               |
| tipo              | enum       | Tipo de personagem                         | 'PC', 'NPC'        | Not Null               |


#### PC

**Descrição**: Contém informações específicas dos personagens jogáveis.

**Observação**: Esta tabela contém chave estrangeira da tabela Sala.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| hp                | int        | Ponto de vida do pc                        | 0-1000             | Not Null               |
| mp                | int        | Pontos de mana do pc                       | 0-1000             | Not Null               |
| xp                | int        | Ponto de experiência do pc                 | 0-1000             | Not Null               |
| absorcao          | int        | Redução do dano que o pc recebe            | 0-1000             | Not Null               |
| atk               | int        | Quantidade de dano básica do pc            | 0-1000             | Not Null               |
| lvl               | int        | Level do pc                                | 1-1000             | Not Null               |
| luck              | int        | Indica a sorte do pc                       | 0-1000             | Not Null               |
| combat_status     | enum       | Indica o estado do pc                      | 'Confuso', 'Envenenado', 'Normal' |Not Null |
| coins             | int        | Indica a quantidaade de moedas do pc       | 0-1000             | Not Null               |
| id_sala           | int        | Indica a sala em o pc está                 | 1-1000             | FK, Not Null           |


#### NPC

**Descrição**: Contém informações específicas dos personagens não jogáveis.

**Observação**: Esta tabela não contém chave estrangeira.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| tipo              | varchar(50)| Indica o tipo de NPC                       | a-z, A-Z           | Not Null               |

##### Mercador

**Descrição**: NPC que comercializa itens.

**Observação**: Esta tabela contém chave estrangeira da tabela Sala.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_sala           | int        | Indica a sala em que o mercador está       | 1-1000             | FK, Not Null           |

##### Contratante

**Descrição**: NPC que fornece contratos para o jogador.

**Observação**: Esta tabela contém chave estrangeira da tabela Sala.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_sala           | int        | Indica a sala em que o contratante está    | 1-1000             | FK, Not Null           |

##### Inimigo

**Descrição**: NPC que participa de combates com o jogador.

**Observação**: Esta tabela não possui chaves estrangeiras.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| hp                | int        | Pontos de vida do inimigo                  | 1-1000             | Not Null               |
| xp                | int        | Pontos de experiência fornecidos ao derrotar o inimigo | 1-1000 | Not Null               |
| absorcao          | int        | Redução do dano que o inimigo recebe       | 1-1000             | Not Null               |
| atk               | int        | Dano básico causado pelo inimigo           | 1-1000             | Not Null               |
| habilidade        | int        | Acréscimo no dano básico do inimigo        | 1-1000             | Not Null               |

##### Chefe

**Descrição**: NPC mais desafiador, geralmente finalizando uma região ou missão.

**Observação**: Esta tabela contém chaves estrangeiras das tabelas Sala e Item.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| hp                | int        | Pontos de vida do chefe                    | 1-1000             | Not Null               |
| xp                | int        | Pontos de experiência fornecidos ao derrotar o chefe  | 1-1000  | Not Null               |
| lvl               | int        | Nível do chefe                             | 1-1000             | Not Null               |
| combat_status     | enum       | Indica o estado do chefe                   | 'Confuso', 'Envenenado', 'Normal' |Not Null |
| absorcao          | int        | Redução do dano que o chefe recebe         | 1-1000             | Not Null               |
| atk               | int        | Dano básico causado pelo inimigo           | 1-1000             | Not Null               |
| item_especial     | int        | Item dropado pelo chefe                    | 1-1000             | FK, Not Null           |
| id_sala           | int        | Indica a sala em que o chefe está          | 1-1000             | FK, Not Null           |

---

### Entidade: Instância Inimigo

**Descrição**: Uma instância de NPC inimigo representa um personagem não jogável que atua como oponente no jogo. 
Essa instância é responsável por gerenciar as interações do inimigo com o ambiente, outros NPCs e o jogador, 
desempenhando um papel essencial na mecânica e na dinâmica de combate do jogo.

**Observação**: Esta tabela contém chaves estrangeiras das tabelas Sala e Inimigo.

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_instancia      | int        | Código de identificação da instância de inimigo    | 1-1000     | PK, Not Null           |
| id_inimigo        | int        | Código de identificação do inimigo         | 1-1000             | FK, Not Null           |
| id_sala           | int        | Código de identificação da sala que a instância de inimigo está | 1-1000  | FK, Not Null |
| vida_atual        | int| Vida atual da instância de inimigo                 | 1-1000             | Not Null               |
| absorcao          | int       | Redução do dano que a instância de inimigo recebe  | 1-1000      | Not Null               |
| atk               | int | Dano básico causado pela isntância de inimigo     | 1-1000             | Not Null               |
| habilidade        | int    | Acréscimo no dano básico do inimigo            | 1-1000             | Not Null               |
| combat_status     | enum       | Indica o estado do chefe                   | 'Confuso', 'Envenenado', 'Normal' |Not Null |

---

### Entidade: Checkpoint

**Descrição**: é um marco no progresso do jogador dentro do jogo, utilizado para salvar o estado atual e permitir que o jogador continue a partir desse ponto em caso de derrota ou ao retornar ao jogo.

**Observação**: Esta tabela contém cahves estrangeiras das tabelas Sala e PC.

| Nome Variável     | Tipo           | Descrição                                    | Valores Permitidos         | Restrições de Domínio      |
|-------------------|----------------|----------------------------------------------|----------------------------|----------------------------|
| id_checkpoint     | int            | Identificador único do checkpoint            | 1-1000                     | PK, Not Null               |
| id_sala           | int            | Referência à sala onde o checkpoint está     | 1-1000                     | FK, Not Null               |
| id_pc             | int            | Referência ao personagem jogável associado   | 1-1000                     | FK, Not Null               |

---

### Entidade: Bibliotacas

**Descrição**: Bibliotacas contidos no jogo

**Observação**: Esta entidade irá armazenas os livros ou conteudos que o jogo oferece, tendo chave estrangeira na tabela Instância item

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_Bibliotacas    | int        | Código de identificação da Bibliotaca      | 1-1000             | PK, Not Null           |
| itens             | int        | Código de instância de itens               | 1-1000             | FK, Not Null           |



---

### Entidade: Bibliotacas

**Descrição**: Bibliotacas contidas nas salas

**Observação**: Esta entidade irá armazenas as Bibliotacas em suas salas, tendo chave estrangeira nas tabelas Bibliotacas e Sala

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_sala           | int        | Código de identificação da sala            | 1-1000             | PK,FK, Not Null        |
| id_Bibliotacas    | int        | Código de identificação da Bibliotacas     | 1-1000             | PK,FK, Not Null        |

---

### Entidade: Sala 

**Descrição**: A sala é contido nas regiões

**Observação**: Esta entidade irá armazenas as salas contidas do game, tendo chaves estrangeiras contidas nas tabelas Sala e Região

| Nome Variável     | Tipo       | Descrição                                  | Valores Permitidos | Restrições de Domínio |
|-------------------|------------|--------------------------------------------|--------------------|------------------------|
| id_sala           | int        | Código de identificação da sala            | 1-1000             | PK, Not Null           |
| id_sala_conectada | int        | Código de identificação da sala conectada  | 1-1000             | FK, Not Null           |
| id_regiao         | int        | Código de identificação da regiao          | 1-1000             | FK, Not Null           |
| nome              | varchar(200) | nome da sala                             | a-z, A-Z           |Not Null                |
| descricao             | varchar(200) | descrição da sala                    | a-z, A-Z           |Not Null                |


---





## Histórico de Versão

| Versão | Data | Descrição | Autor(es) |
| :----: | :--: | :-------: | :-------: | 
| `1.0`  | 02/05/2025 | Primeira versão  do DD  | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr)  |


