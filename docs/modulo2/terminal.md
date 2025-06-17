
# Detalhamento do Código: Terminal Interativo de RPG

Este documento apresenta o detalhamento do código para um terminal de RPG em Python. A aplicação foca na criação de personagens e na navegação por um mundo persistente, com todas as interações gerenciadas por um banco de dados.

## 📋 Funcionalidades Principais

### 1\. **Menu Principal**

  - Apresenta a porta de entrada do jogo, oferecendo as opções iniciais ao jogador.
  - Direciona o fluxo do programa com base na escolha do usuário.
  - **Função**: `main_menu()`

**Exemplo de Saída:**

```
========================================
      BEM-VINDO AO JOGO DE TERMINAL
========================================

Escolha uma opção:
  [1] Criar Novo Personagem
  [2] Iniciar Jogo
  [3] Sair

----------------------------------------
Sua escolha:
```

### 2\. **Criação de Personagem**

  - Permite que um novo jogador crie seu personagem no jogo.
  - Solicita um nome e o salva no banco de dados através de uma função dedicada.
  - Impede a criação de personagens com nomes vazios.
  - **Função**: `criar_personagem()`

**Fluxo de Uso:**

  - O jogador seleciona a opção "Criar Novo Personagem" no menu.
  - Digita o nome desejado e o sistema o registra no banco de dados.

**Exemplo de Saída:**

```
--- CRIAÇÃO DE PERSONAGEM ---

Digite o nome do seu personagem: Alucard

Personagem 'Alucard' criado com sucesso!
```

### 3\. **Seleção de Personagem e Início de Jogo**

  - Lista todos os personagens já criados e disponíveis no banco de dados.
  - Permite ao jogador selecionar com qual personagem deseja entrar no mundo do jogo.
  - Inicia o loop principal do jogo (`game_loop`) após uma seleção válida.
  - **Função**: `iniciar_jogo()`

**Exemplo de Saída:**

```
--- INICIAR JOGO ---

Selecione um personagem para continuar:

[1] - Alucard
[2] - Richter

Digite o ID do personagem: 1
```

### 4\. **Navegação e Loop Principal do Jogo**

  - Constitui o núcleo da experiência de jogo, onde o jogador explora o mundo.
  - A cada turno, a tela é limpa e o cenário atual é exibido, incluindo o nome e a descrição do local.
  - As saídas (caminhos) disponíveis são listadas em um menu numerado, facilitando a movimentação.
  - O jogador se move escolhendo o número correspondente à direção desejada.
  - **Função**: `game_loop(personagem_id, personagem_nome)`

**Exemplo de Saída:**

```
--- Alucard ---
Você está em: Grande Salão
Um salão imponente com um trono ao fundo e tapeçarias antigas nas paredes.

--------------------
O que você faz?

  [1] Ir para o Corredor Leste
  [2] Subir a Escadaria Principal
  [3] Voltar ao menu principal

--------------------
Sua escolha: 1
```

-----

## 📜 Estrutura do Código

  - **`main_menu()`**:
      - Gerencia o menu inicial do jogo, permitindo criar um personagem, iniciar uma partida ou sair.
  - **`criar_personagem()`**:
      - Lida com a interface e a lógica para registrar um novo personagem no banco de dados.
  - **`iniciar_jogo()`**:
      - Busca e exibe os personagens existentes para seleção e inicia o loop principal do jogo.
  - **`game_loop(personagem_id, personagem_nome)`**:
      - O coração do jogo. Busca os detalhes da localização atual do personagem no banco de dados.
      - Exibe a descrição do local e as saídas disponíveis como um menu de múltipla escolha.
      - Processa a entrada do jogador para movimentação ou para sair para o menu principal.
  - **`clear_screen()`**:
      - Função utilitária para limpar a tela do terminal, compatível com Windows (`cls`) e Unix (`clear`).
  - **Módulo `database`**:
      - O código depende de um módulo externo (`database.py`) que contém funções essenciais para a comunicação com o banco de dados, como `get_all_characters`, `get_location_details` e `call_db_function`.

-----

## 🛠️ Configuração Necessária

1.  **Banco de Dados**:

      - É essencial ter um banco de dados (provavelmente PostgreSQL, com base na menção ao Docker no código) ativo e acessível.
      - O banco de dados deve conter as tabelas e funções necessárias, como `criar_personagem` e `mover_personagem`.

2.  **Dependências**:

      - O código utiliza as bibliotecas padrão `os` e `time`.
      - Requer um módulo local chamado `database.py`, que deve ser criado para encapsular todas as chamadas ao banco de dados (ex: usando `psycopg2` para PostgreSQL).

3.  **Execução**:

      - Salve o código principal em um arquivo, por exemplo, `main.py`.
      - Certifique-se de que o arquivo `database.py` esteja no mesmo diretório.
      - Execute o script a partir do terminal:
        ```bash
        python main.py
        ```
      - O código inclui uma verificação inicial (`get_all_characters()`) para garantir que a conexão com o banco de dados está funcional antes de exibir o menu principal.

-----

## 🔧 Possíveis Melhorias Futuras

  - **Sistema de Status**: Exibir atributos do personagem (HP, MP, Nível) no `game_loop`.
  - **Combate**: Implementar um sistema de encontros com inimigos nas salas.
  - **Inventário e Itens**: Adicionar a capacidade de coletar, gerenciar e usar itens.
  - **Interações**: Permitir que o jogador interaja com NPCs, baús e outros elementos do cenário.
  - **Missões (Quests)**: Desenvolver um sistema de missões com objetivos e recompensas.

-----

## Histórico de Versão

| Versão | Data       | Descrição                                         | Autor(es)      |
| :----: | :--------- | :-------------------------------------------------- | :------------- |
| `1.0`  | 17/06/2025 | Versão inicial com criação e navegação de personagem. | [Emivalto da Costa Tavares Junior](https://github.com/EmivaltoJrr) |