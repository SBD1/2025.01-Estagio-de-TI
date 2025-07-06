CREATE OR REPLACE FUNCTION validar_limite_inventario()
RETURNS TRIGGER AS $$
DECLARE
    v_id_item INT;
    v_id_inventario INT := NEW.id_inventario;
    v_quantidade_nova INT := NEW.quantidade;
    v_quantidade_existente INT := 0;
    v_quantidade_total INT;
    v_espaco_total INT;
    v_espacos_usados INT := 0;
    v_espacos_necessarios INT := 0;
    v_tipo TEXT;
BEGIN
    -- Pega o tipo e id_item da instância sendo inserida
    SELECT it.id_item, it.tipo INTO v_id_item, v_tipo
    FROM InstanciaItem iit
    JOIN Item it ON iit.id_item = it.id_item
    WHERE iit.id_instancia = NEW.id_instancia;

    -- Verifica a quantidade atual do mesmo item já no inventário (empilhamento)
    SELECT COALESCE(SUM(ii.quantidade), 0) INTO v_quantidade_existente
    FROM ItemInventario ii
    JOIN InstanciaItem iit ON ii.id_instancia = iit.id_instancia
    WHERE ii.id_inventario = v_id_inventario AND iit.id_item = v_id_item;

    v_quantidade_total := v_quantidade_existente + v_quantidade_nova;

    -- Calcula espaços adicionais que essa inserção causaria
    IF v_tipo = 'Arma' THEN
        v_espacos_necessarios := v_quantidade_nova;
    ELSE
        -- Exemplo: já tinha 20, vai pra 21 → antes ocupava 1, agora ocupa 2
        v_espacos_necessarios := CEIL(v_quantidade_total / 20.0) - CEIL(v_quantidade_existente / 20.0);
    END IF;

    -- Soma o espaço já ocupado por todos os outros itens no inventário
    SELECT COALESCE(SUM(
        CASE 
            WHEN it.tipo = 'Arma' THEN ii.quantidade
            ELSE CEIL(ii.quantidade / 20.0)
        END
    ), 0) INTO v_espacos_usados
    FROM ItemInventario ii
    JOIN InstanciaItem iit ON ii.id_instancia = iit.id_instancia
    JOIN Item it ON it.id_item = iit.id_item
    WHERE ii.id_inventario = v_id_inventario;

    -- Soma o espaço novo que será ocupado por esta adição
    v_espacos_usados := v_espacos_usados + v_espacos_necessarios;

    -- Obtém o espaço máximo permitido
    SELECT espaco_total INTO v_espaco_total
    FROM Inventario
    WHERE id_inventario = v_id_inventario;

    -- Verifica se ultrapassa o limite
    IF v_espacos_usados > v_espaco_total THEN
        RAISE EXCEPTION 'Inventário cheio: necessário %, disponível %', v_espacos_usados, v_espaco_total;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_validar_limite_inventario ON ItemInventario;

CREATE TRIGGER trigger_validar_limite_inventario
BEFORE INSERT ON ItemInventario
FOR EACH ROW
EXECUTE FUNCTION validar_limite_inventario();


CREATE OR REPLACE FUNCTION validar_limite_inventario_update()
RETURNS TRIGGER AS $$
DECLARE
    v_id_item INT;
    v_id_inventario INT;
    v_quantidade_nova INT := NEW.quantidade;
    v_quantidade_antiga INT := OLD.quantidade;
    v_quantidade_total INT;
    v_espaco_total INT;
    v_espacos_usados INT := 0;
    v_espacos_necessarios INT := 0;
    v_tipo TEXT;
BEGIN
    v_id_inventario := NEW.id_inventario;

    -- Pega tipo e id_item
    SELECT it.id_item, it.tipo INTO v_id_item, v_tipo
    FROM InstanciaItem iit
    JOIN Item it ON it.id_item = iit.id_item
    WHERE iit.id_instancia = NEW.id_instancia;

    -- Soma todas as quantidades desse item no inventário, excluindo a linha que será atualizada
    SELECT COALESCE(SUM(ii.quantidade), 0) INTO v_quantidade_total
    FROM ItemInventario ii
    JOIN InstanciaItem iit ON iit.id_instancia = ii.id_instancia
    WHERE ii.id_inventario = v_id_inventario
      AND iit.id_item = v_id_item
      AND ii.id_instancia <> NEW.id_instancia;

    -- Soma quantidade nova (após update)
    v_quantidade_total := v_quantidade_total + v_quantidade_nova;

    -- Espaço necessário para este item atualizado
    IF v_tipo = 'Arma' THEN
        v_espacos_necessarios := v_quantidade_nova;
    ELSE
        v_espacos_necessarios := CEIL(v_quantidade_total / 20.0);
    END IF;

    -- Soma espaços usados para todos os outros itens
    SELECT COALESCE(SUM(
        CASE
            WHEN it.tipo = 'Arma' THEN ii.quantidade
            ELSE CEIL(ii.quantidade / 20.0)
        END
    ), 0) INTO v_espacos_usados
    FROM ItemInventario ii
    JOIN InstanciaItem iit ON iit.id_instancia = ii.id_instancia
    JOIN Item it ON it.id_item = iit.id_item
    WHERE ii.id_inventario = v_id_inventario
      AND ii.id_instancia <> NEW.id_instancia;

    -- Total espaços usados depois do update
    v_espacos_usados := v_espacos_usados + v_espacos_necessarios;

    -- Espaço total do inventário
    SELECT espaco_total INTO v_espaco_total FROM Inventario WHERE id_inventario = v_id_inventario;

    IF v_espacos_usados > v_espaco_total THEN
        RAISE EXCEPTION 'Espaço insuficiente no inventário após atualização! Necessário: %, Disponível: %', v_espacos_usados, v_espaco_total;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trigger_validar_limite_inventario_update ON ItemInventario;

CREATE TRIGGER trigger_validar_limite_inventario_update
BEFORE UPDATE ON ItemInventario
FOR EACH ROW
EXECUTE FUNCTION validar_limite_inventario_update();



