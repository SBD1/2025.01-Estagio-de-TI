# MER - Modelo Entidade Relacionamento

## Introdução

O Modelo Entidade-Relacionamento (MER) é uma representação conceitual utilizada para modelar a estrutura de um banco de dados. Ele descreve as entidades relevantes em um determinado domínio de negócio, juntamente com seus atributos e os relacionamentos existentes entre elas.

Em resumo, o Modelo Entidade-Relacionamento é uma ferramenta essencial no planejamento e desenvolvimento de sistemas de informação, pois proporciona uma modelagem conceitual clara e estruturada dos elementos e suas interações, servindo como base para a implementação efetiva do banco de dados.

> Entidades: os objetos da realidade a ser modelada.<br>
> Atributos: características específicas de uma entidade.<br>
> Relacionamentos: as associações entre as entidades.<br>



# Modelo Entidade-Relacionamento - Jogo Estagiário de TI

## Entidades e Atributos

### Prota
- *id_prota*
- reputação
- stress
- coins

### Mochila
- *id_prota*
- ocupabilidade
- qt_itens

### Missão
- *id_missao*
- nome
- descrição

### Demanda
- *id_demanda*

### Tarefa
- *id_tarefa*

### Fracasso
- *id_derrota*
- causa
- momento

### Personagem (generalização)
- *id_personagem*
- nome
- descrição

### Chefe (especialização de Personagem)

### Colegas de Trabalho (especialização de Personagem)

### Instância Colegas
- *id_instancia_colega*
- nome

### Sala
- *id_sala*

### Diálogo
- *id_dialogo*
- texto

### Andar
- *id_andar*
- número
- restrito

### Prédio
- *id_prédio*

### Mundo
- *id_mundo*

### Cafeteria
- *id_cafeteria*
- itens_disponíveis
- aberta

### Almoxarife (especialização de Personagem)

### Almoxarifado
- *id_almoxarifado*

### Item (generalização)
- *id_item*
- nome
- descrição
- preço
- eh_unico
- tipo

#### Conhecimento (especialização de Item)
#### Hardware (especialização de Item)
#### Consumíveis (especialização de Item)

### Instância Item
- *id_instancia*
- id_item
- proprietário
- localização

### Checkpoint

## Relacionamentos

- **Prota** `1:1` — Possui — `1:1` **Mochila**
- **Prota** `1:1` — Tem — `0:N` **Missão**
- **Missão** `1:N` — Generaliza — **Demanda** e **Missão**
- **Prota** `1:1` — Fracassa — `1:1` **Fracasso**
- **Prota** `1:N` — Negocia — `1:N` **Almoxarife**
- **Almoxarife** `1:1` — Trabalha em — `1:1` **Almoxarifado**
- **Almoxarifado** `1:1` — Contém — `0:N` **Item**
- **Item** `1:N` — Está em — `1:N` *Instância Item**
- **Instância Item** `0:N` — Pertence a — `1:1` **Item**
- **Item** `1:N` — Fornece — `1:N` **Conhecimento | Hardware | Consumíveis**
- **Item** `1:N` — Envolve — `1:N` **Missão**
- **Personagem** `1:N` — Executa — `0:N` **Diálogo**
- **Sala** `1:N` — Contém — `1:1` **Diálogo**
- **Sala** `1:N` — Está em — `1:1` **Andar**
- **Andar** `1:1` — Contém — `1:N` **Sala**
- **Andar** `1:N` — Está em — `1:1` **Prédio**
- **Prédio** `1:1` — Contém — `1:N` **Andar**
- **Prédio** `1:1` — Está em — `1:1` **Mundo**
- **Mundo** `1:1` — Contém — `1:1` **Prédio**
- **Mundo** `1:1` — Contém — `1:1` **Cafeteria**
- **Cafeteria** `1:1` — Oferece — `0:N` **Item**
- **Personagem** `1:N` — Está em — `0:N` **Sala**
- **Prota** `1:1` — Está em — `1:1` **Sala**
- **Instância Colegas** `0:N` — Está em — `0:N` **Sala**
- **Instância Colegas** `0:N` — Composta por — `0:N` **Personagem**
- **Instância Colegas** `0:N` — Tem checkpoint — `1:1` **Checkpoint**
- **Personagem** `1:N` — Libera — `0:N` **Sala**
- **Prota** `1:N` — Libera — `0:N` **Sala**
- **Prota** `1:1` — Fracassa — `1:1` **Missão**

---



## Histórico de Versão

| Versão | Data | Descrição | Autor(es) | Revisor |
| :-: | :-: | :-: | :-: | :-: |
| `1.0`  | 02/05/2025 | Primeira versão  do MER  | [Gabriel Basto Bertolazi](https://github.com/Bertolazi) | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr) |
| `1.1`  | 02/05/2025 | Adicionando MER | [Caio M](https://github.com/Caiomesvie) | [Gabriel Basto Bertolazi](https://github.com/Bertolazi)  |



