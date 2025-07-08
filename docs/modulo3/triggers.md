# Triggers no Banco de Dados

As triggers (gatilhos) são ferramentas essenciais no banco de dados do jogo, atuando como guardiãs da integridade dos dados e da automação de regras de negócio. Elas são executadas automaticamente em resposta a eventos específicos (como `INSERT` ou `UPDATE`), garantindo que o estado do jogo permaneça consistente sem a necessidade de lógica adicional no código da aplicação.

## Triggers Implementadas

### 1. `trigger_criar_inventario`

Esta trigger está associada à tabela `Estagiario` e desempenha um papel fundamental na criação de novos personagens.

-   **Evento:** `AFTER INSERT ON Estagiario`
-   **Ação:** Executa a função `criar_inventario_estagiario()`
-   **Código:**
    ```sql
    CREATE TRIGGER trigger_criar_inventario
    AFTER INSERT ON Estagiario
    FOR EACH ROW
    EXECUTE FUNCTION criar_inventario_estagiario();
    ```
-   **Funcionalidade:** Assim que um novo estagiário é inserido na tabela `Estagiario`, esta trigger é disparada automaticamente para criar uma entrada correspondente na tabela `Inventario`. Isso garante que todo jogador, desde o momento de sua criação, possua um inventário pronto para receber itens, com uma capacidade inicial definida (12 espaços).

### 2. Triggers de Validação de Tipo de Item

Este conjunto de triggers garante a integridade lógica da modelagem de itens. Como um item pode ser de um, e apenas um, tipo especializado (`PowerUp`, `Consumivel`, ou `Equipamento`), estas triggers impedem inserções ou atualizações que violem essa regra.

-   **Evento:** `BEFORE INSERT OR UPDATE` nas tabelas `PowerUp`, `Consumivel`, e `Equipamento`.
-   **Ação:** Todas executam a mesma função de validação: `verificar_item_tipo_unico()`.
-   **Código:**
    ```sql
    -- Exemplo para a tabela PowerUp
    CREATE TRIGGER validar_tipo_powerup
    BEFORE INSERT OR UPDATE ON PowerUp
    FOR EACH ROW
    EXECUTE FUNCTION verificar_item_tipo_unico();
    ```
    *(Triggers análogas existem para as tabelas `Consumivel` e `Equipamento`)*
-   **Funcionalidade:** Antes de permitir uma inserção ou atualização em uma tabela de item especializado (ex: `PowerUp`), a função `verificar_item_tipo_unico` consulta a tabela `Item` para verificar o tipo do item. Se houver uma tentativa de registrar um item em uma tabela de tipo incorreto (ex: cadastrar um item do tipo 'Equipamento' na tabela `Consumivel`), a trigger impede a operação e levanta uma exceção, prevenindo a corrupção de dados.

## Melhorias Implementadas

A utilização de triggers representa uma melhoria substancial na arquitetura do banco de dados, trazendo mais robustez e automação.

-   **Automação e Consistência:** A `trigger_criar_inventario` elimina a necessidade do código da aplicação se lembrar de criar um inventário toda vez que um personagem é criado. Isso reduz a chance de erros e garante que a regra de negócio ("todo estagiário tem um inventário") seja sempre aplicada no nível do banco de dados.
-   **Integridade Referencial Lógica:** As triggers de validação de tipo de item implementam uma regra de negócio complexa que não poderia ser modelada apenas com constraints de chave estrangeira. Elas garantem que a especialização da entidade `Item` seja mutuamente exclusiva, prevenindo dados ilógicos e simplificando as consultas futuras, pois pode-se confiar que um `id_item` não aparecerá em múltiplas tabelas de tipo.