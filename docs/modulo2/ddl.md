# DDL - Data Definition Language

## Introdução

A DDL (Data Definition Language) é a linguagem utilizada para definir e modificar a estrutura dos objetos em um banco de dados. No jogo Estágio de TI, ela é essencial para criar as tabelas que armazenam os dados do jogo, estabelecer os relacionamentos entre as entidades, definir restrições de integridade, configurar chaves e índices, e também para criar funções e procedimentos armazenados. Essas definições formam a estrutura base do banco de dados do jogo, permitindo funcionalidades fundamentais como a navegação pelo mundo do jogo,

## Migrações do Banco de Dados

### V1__Mundo_table.sql
```sql
CREATE TABLE IF NOT EXISTS Mundo (
    id_mundo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);
```

### V2__Andar_table.sql
```sql
CREATE TABLE IF NOT EXISTS Andar (
    id_andar SERIAL PRIMARY KEY,
    id_mundo INT NOT NULL, 
    numero SMALLINT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_mundo) REFERENCES Mundo(id_mundo)
);
```

### V3__Sala_table.sql
```sql
CREATE TABLE IF NOT EXISTS Sala (
    id_sala SERIAL PRIMARY KEY,
    id_andar INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    FOREIGN KEY (id_andar) REFERENCES Andar(id_andar)
);
```

### V4__Cafeteria_table.sql
```sql
CREATE TABLE IF NOT EXISTS Cafeteria (
    id_cafeteria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL DEFAULT 'Café do Estágio',
    aberto BOOLEAN NOT NULL DEFAULT TRUE,
    descricao TEXT
);
```

### V5__Personagem_table.sql
```sql
CREATE TABLE IF NOT EXISTS Personagem (
    id_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('PC', 'NPC')),
    descricao VARCHAR(200)
);
```

### V6__NPC_table.sql
```sql
CREATE TABLE IF NOT EXISTS NPC (
    id_personagem INT PRIMARY KEY,
    tipo VARCHAR(10) NOT NULL,
    andar_atual INT,
    dialogo_padrao VARCHAR(300) NOT NULL,
    FOREIGN KEY (id_personagem) REFERENCES Personagem(id_personagem),
    FOREIGN KEY (andar_atual) REFERENCES Andar(id_andar)
);
```

### V7__Estagiario_table.sql
```sql
CREATE TABLE IF NOT EXISTS Estagiario (
    id_personagem SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    xp INT NOT NULL CHECK (xp BETWEEN 0 AND 10000),
    nivel INT NOT NULL CHECK (nivel >= 1 AND nivel <= 100),
    respeito INT DEFAULT 0 CHECK (respeito >= 0 AND respeito <= 100),
    coins INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Normal', 'Confuso', 'Estressado', 'Motivado')),
    andar_atual INT,
    sala_atual INT,
    FOREIGN KEY (andar_atual) REFERENCES Andar(id_andar),
    FOREIGN KEY (sala_atual) REFERENCES Sala(id_sala),
    CONSTRAINT UQ_Estagiario_Nome UNIQUE(nome)
);
```

### V9__Item_table.sql
```sql
CREATE TABLE IF NOT EXISTS Item (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('PowerUp', 'Consumivel', 'Equipamento')),
    preco_base INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS PowerUp (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    bonus_ataque INT,
    duracao INT
);

CREATE TABLE IF NOT EXISTS Consumivel (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    recuperacao_vida INT
);

CREATE TABLE IF NOT EXISTS Equipamento (
    id_item INT PRIMARY KEY REFERENCES Item(id_item) ON DELETE CASCADE,
    slot VARCHAR(50),
    bonus_permanente INT
);

CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia SERIAL PRIMARY KEY,
    id_item INT REFERENCES Item(id_item),
    quantidade INT DEFAULT 1,
    local_atual VARCHAR(20) CHECK (local_atual IN ('Inventario', 'Chao', 'Loja'))
);
```

### V10__Inventario_table.sql
```sql
CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_estagiario INT NOT NULL UNIQUE,
    espaco_total INT NOT NULL DEFAULT 12,
    espaco_usado INT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);

CREATE TABLE IF NOT EXISTS ItemInventario (
    id_inventario INT,
    id_instancia INT,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_inventario, id_instancia),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario),
    FOREIGN KEY (id_instancia) REFERENCES InstanciaItem(id_instancia)
);
```

### V11__Inimigo_table.sql
```sql
CREATE TABLE IF NOT EXISTS Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ataque VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS InstanciaInimigo (
    id_instancia SERIAL PRIMARY KEY,
    id_inimigo INT NOT NULL,
    vida INT NOT NULL,
    dano INT NOT NULL,
    FOREIGN KEY (id_inimigo) REFERENCES Inimigo(id_inimigo)
);
```

### V15__Combate_table.sql
```sql
CREATE TABLE IF NOT EXISTS Combate (
    id_combate SERIAL PRIMARY KEY,

    id_estagiario INT NOT NULL,
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem),

    id_npc INT NOT NULL,
    FOREIGN KEY (id_npc) REFERENCES NPC(id_personagem),

    resultado VARCHAR(20) NOT NULL CHECK (resultado IN ('venceu', 'derrotado', 'fugiu')),
    data TIMESTAMP DEFAULT NOW()
);
```

### V28__Missao_table.sql
```sql
CREATE TABLE IF NOT EXISTS Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    dialogo_inicial TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('Combate', 'Entrega', 'Conversa', 'Manutenção')),
    xp_recompensa INT NOT NULL,
    moedas_recompensa INT NOT NULL,
    npc_origem INT NOT NULL,
    FOREIGN KEY (npc_origem) REFERENCES NPC(id_personagem)
);

CREATE TABLE IF NOT EXISTS MissaoStatus (
    id_missao INT,
    id_estagiario INT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Disponível', 'Em Andamento', 'Concluída')),
    PRIMARY KEY (id_missao, id_estagiario),
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao),
    FOREIGN KEY (id_estagiario) REFERENCES Estagiario(id_personagem)
);
```




## Histórico de Versão

| Versão | Data | Descrição | Autor(es) | Revisor |
|:--:|:--:|:--:|:--:|:--:|
| 1.0 | 16/06/2025 | Criação do documento DDL com versionamento | [Lucas Mendonça Arruda](https://github.com/lucasarruda9) | [Gabriel Basto Bertolazi](https://github.com/Bertolazi)|