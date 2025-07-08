# Funcionamento do Jogo: A Saga do Estagiário

## Visão Geral

"A Saga do Estagiário" é um RPG de texto interativo, desenvolvido em Python, onde o jogador assume o papel de um estagiário de TI em uma grande corporação. O objetivo final é progredir na carreira, superando desafios em diferentes andares do prédio, para alcançar a tão sonhada efetivação como Desenvolvedor Júnior.

O jogo é executado em um terminal e utiliza um banco de dados PostgreSQL, gerenciado com Docker, para garantir a persistência de dados dos personagens, missões e do mundo do jogo.

## Mecânicas Principais

O fluxo do jogo é centrado em um loop principal que se atualiza a cada ação do jogador, apresentando um menu de opções dinâmico com base no contexto atual.

-   **Criação e Carregamento:** O jogador pode criar um novo personagem ou carregar um já existente. Cada personagem tem seus próprios status, inventário e progresso de missões.
-   **Exploração:** O jogador navega entre as salas e andares do prédio. A descrição de cada local e as saídas disponíveis são carregadas dinamicamente do banco de dados.
-   **Interação com NPCs:** É possível conversar com diversos personagens (NPCs). Os diálogos são contextuais, mudando conforme o jogador aceita ou progride em missões, tornando o mundo mais vivo e reativo.
-   **Missões e Tarefas:** O núcleo da progressão do jogo. As missões podem ser de diferentes tipos: `Combate`, `Entrega`, `Conversa` ou `Manutenção`, cada uma com seus próprios objetivos e recompensas em XP e moedas.
-   **Combate:** Em certas áreas, o jogador pode encontrar inimigos como "Bugs" ou "Malware". O combate é baseado em turnos, onde os atributos de ataque e defesa do jogador e do inimigo determinam o resultado.
-   **Inventário e Itens:** O jogador pode adquirir itens, seja comprando em lojas como a Cafeteria, seja como recompensa. É possível gerenciar o inventário para usar itens consumíveis (que recuperam vida), equipar itens que melhoram os status (ataque/defesa) ou desequipá-los.

## Melhorias Implementadas

A versão atual do jogo é um avanço significativo em relação aos modelos base iniciais.

-   **De Estático para Dinâmico:** O fluxo de jogo deixou de ser um menu de opções fixo para se tornar um sistema dinâmico. As ações disponíveis (falar, lutar, mover-se) agora dependem diretamente do ambiente e dos NPCs ou inimigos presentes na sala, tornando a exploração mais orgânica e interessante.
-   **Interatividade Aprofundada:** A interatividade foi expandida para além da simples navegação. A implementação de um sistema de combate, diálogos contextuais e, mais notavelmente, um inventário totalmente funcional (com uso e equipamento de itens) adicionou camadas estratégicas e de personalização ao jogo, que eram inexistentes anteriormente.
-   **Centralização da Lógica de Jogo:** Grande parte da lógica que define a experiência do jogador (o que ele vê, para onde pode ir, com quem pode falar) foi movida para o banco de dados e é acessada através de Stored Procedures (Funções). Isso tornou o código da aplicação Python mais limpo e focado na interface, enquanto o banco de dados gerencia as regras do mundo do jogo.