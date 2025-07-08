# Stored Procedures (Funções)

As Stored Procedures, implementadas no PostgreSQL como Funções, são o cérebro da lógica de negócio do jogo. Elas encapsulam operações complexas, desde a criação de um personagem até a conclusão de uma missão, diretamente no banco de dados. Isso promove segurança, reutilização de código e melhora o desempenho ao reduzir a comunicação entre a aplicação e o banco.

## Funções Principais

### Funções de Personagem e Mundo

-   **`criar_personagem(p_nome_personagem VARCHAR)`:** Cria um novo estagiário, define seus atributos iniciais, o posiciona na sala de partida e cria seu inventário (via trigger). Trata nomes duplicados para evitar erros.
-   **`descrever_local_detalhado(p_id_personagem INT)`:** Retorna uma descrição completa da localização atual do jogador, incluindo nome do andar/sala, descrição e uma lista de todas as saídas possíveis. Centraliza a lógica de exploração.
-   **`mover_personagem(p_id_personagem INT, p_direcao_texto VARCHAR)`:** Atualiza a localização do jogador para uma nova sala adjacente.
-   **`usar_elevador(p_id_personagem INT, p_andar_destino INT)`:** Gerencia a movimentação entre andares, verificando se o jogador está em uma 'Sala Central' para acessar o elevador.

### Funções de Itens e Inventário

-   **`comprar_item(p_id_estagiario INT, p_id_instancia INT, p_quantidade INT)`:** Orquestra toda a lógica de uma compra: verifica o saldo de moedas, a disponibilidade do item, debita o valor, adiciona o item ao inventário e atualiza o estoque da loja. Tudo isso em uma única transação atômica.
-   **`usar_item(p_id_estagiario INT, p_id_instancia INT)`:** Aplica o efeito de um item consumível (cura) ou de um `PowerUp` (bônus de ataque) e remove o item do inventário do jogador.
-   **`equipar_item(p_id_estagiario INT, p_id_instancia INT)`:** Move um item de equipamento do inventário para um slot equipado, aplicando seus bônus de ataque e defesa aos status do jogador e validando se o slot está livre.
-   **`desequipar_item(p_id_estagiario INT, p_id_instancia INT)`:** Remove os bônus de um item equipado e o retorna para o inventário do jogador.

### Funções de Missão

-   **`concluir_missao(p_id_estagiario INT, p_id_missao INT)`:** Gerencia o processo de finalização de uma missão. Ela atualiza o status da missão para 'Concluída', insere um registro na tabela `MissaoConcluida`, e adiciona as recompensas de XP e moedas aos atributos do jogador, garantindo consistência transacional.

## Melhorias Implementadas

A adoção extensiva de Stored Procedures foi uma das melhorias arquiteturais mais significativas do projeto.

-   **Encapsulamento e Reutilização:** A lógica de negócio crítica, como o complexo processo de compra ou a conclusão de uma missão, foi movida do código Python para funções no banco de dados. Isso significa que a aplicação apenas chama a função (ex: `comprar_item(...)`) sem precisar conhecer os detalhes da implementação, tornando o código Python mais limpo e a lógica de negócio reutilizável e consistente.
-   **Segurança e Atomicidade:** Operações que envolvem múltiplas tabelas, como `comprar_item` ou `concluir_missao`, são tratadas como transações atômicas dentro das funções. Se qualquer passo falhar, toda a operação é revertida (`ROLLBACK`), garantindo que o banco de dados nunca fique em um estado inconsistente. Isso é muito mais seguro e robusto do que gerenciar transações manualmente no código da aplicação.
-   **Implementação de Novas Mecânicas:** A principal melhoria foi a possibilidade de implementar mecânicas de jogo inteiramente novas. As funções `usar_item`, `equipar_item` e `desequipar_item` não existiam antes e foram criadas para dar vida ao sistema de inventário, adicionando uma camada de estratégia e profundidade que transformou a experiência de jogo.