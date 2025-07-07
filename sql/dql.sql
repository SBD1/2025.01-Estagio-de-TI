CREATE OR REPLACE FUNCTION criar_personagem(
    p_nome_personagem VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_sala_inicial RECORD;
    v_id_personagem INT;
BEGIN
    -- Passo 1: Insere na tabela base 'Personagem' para obter um ID.
    -- A constraint de nome único na tabela Personagem vai gerar o erro aqui.
    INSERT INTO Personagem (nome, tipo, descricao)
    VALUES (p_nome_personagem, 'PC', 'Um novo estagiário pronto para os desafios.')
    RETURNING id_personagem INTO v_id_personagem;

    -- Passo 2: Encontra a sala inicial (Térreo)
    SELECT id_sala, id_andar INTO v_sala_inicial
    FROM vw_sala_central --uma view
    WHERE numero_andar = 0;

    -- Passo 3: Insere na tabela especializada 'Estagiario' usando o ID obtido
    INSERT INTO Estagiario(
        id_personagem,
        xp, nivel, respeito, coins, ataque, defesa, vida, status,
        andar_atual, sala_atual
    ) VALUES (
        v_id_personagem,
        0, 1, 50, 100, 10, 5, 100, 'Normal',
        v_sala_inicial.id_andar, v_sala_inicial.id_sala
    );

    RETURN 'Estagiário "' || p_nome_personagem || '" criado com sucesso! (ID: ' || v_id_personagem || ')';

EXCEPTION
    WHEN unique_violation THEN
        RETURN 'Erro: Já existe um personagem com este nome.';
    WHEN OTHERS THEN
        RETURN 'Erro inesperado ao criar estagiário: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION criar_inventario_estagiario()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Inventario (id_estagiario, espaco_total)
    VALUES (NEW.id_personagem, 12);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_criar_inventario
AFTER INSERT ON Estagiario
FOR EACH ROW
EXECUTE FUNCTION criar_inventario_estagiario();


CREATE OR REPLACE FUNCTION descrever_local_detalhado(
    p_id_personagem INT
) RETURNS TABLE(nome_local TEXT, descricao TEXT, saidas TEXT[]) AS $$
DECLARE
    v_posicao RECORD;
BEGIN
    SELECT * INTO v_posicao
    FROM vw_posicao_estagiario
    WHERE id_personagem = p_id_personagem;

    RETURN QUERY
    WITH saidas_possiveis AS (
        SELECT 'Ir para ' || nome_sala_destino as direcao
        FROM vw_conexoes_salas
        WHERE id_sala_origem = v_posicao.sala_atual
        UNION ALL
        SELECT 'Chamar Elevador'
        WHERE v_posicao.nome_sala = 'Sala Central'
    )
    SELECT
        (v_posicao.nome_andar || E'\nSala: ' || v_posicao.nome_sala),
        v_posicao.descricao_sala,
        ARRAY(
            SELECT direcao
            FROM saidas_possiveis
            WHERE direcao IS NOT NULL
            ORDER BY direcao
        );
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION mover_personagem(
    p_id_personagem INT,
    p_direcao_texto VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_posicao RECORD;
    v_nova_sala INT;
BEGIN
    SELECT * INTO v_posicao
    FROM vw_posicao_estagiario
    WHERE id_personagem = p_id_personagem;

    IF p_direcao_texto LIKE 'Ir para%' THEN
        SELECT id_sala_destino INTO v_nova_sala
        FROM vw_conexoes_salas
        WHERE id_sala_origem = v_posicao.sala_atual
        AND 'Ir para ' || nome_sala_destino = p_direcao_texto;

        IF v_nova_sala IS NOT NULL THEN
            UPDATE Estagiario
            SET sala_atual = v_nova_sala
            WHERE id_personagem = p_id_personagem;
            RETURN 'Você se moveu para outra sala.';
        END IF;
    END IF;

    RETURN 'Movimento inválido.';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION verificar_item_tipo_unico() RETURNS TRIGGER AS $$
DECLARE
    tipo_item TEXT;
    count_tipos INT := 0;
BEGIN
    SELECT tipo INTO tipo_item FROM Item WHERE id_item = NEW.id_item;

    IF tipo_item = 'PowerUp' THEN
        SELECT COUNT(*) INTO count_tipos FROM Consumivel WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo PowerUp não pode estar também como Consumivel.';
        END IF;
        SELECT COUNT(*) INTO count_tipos FROM Equipamento WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo PowerUp não pode estar também como Equipamento.';
        END IF;
    ELSIF tipo_item = 'Consumivel' THEN
        SELECT COUNT(*) INTO count_tipos FROM PowerUp WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo Consumivel não pode estar também como PowerUp.';
        END IF;
        SELECT COUNT(*) INTO count_tipos FROM Equipamento WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo Consumivel não pode estar também como Equipamento.';
        END IF;
    ELSIF tipo_item = 'Equipamento' THEN
        SELECT COUNT(*) INTO count_tipos FROM PowerUp WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo Equipamento não pode estar também como PowerUp.';
        END IF;
        SELECT COUNT(*) INTO count_tipos FROM Consumivel WHERE id_item = NEW.id_item;
        IF count_tipos > 0 THEN
            RAISE EXCEPTION 'Item do tipo Equipamento não pode estar também como Consumivel.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validar_tipo_powerup
BEFORE INSERT OR UPDATE ON PowerUp
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();

CREATE TRIGGER validar_tipo_consumivel
BEFORE INSERT OR UPDATE ON Consumivel
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();

CREATE TRIGGER validar_tipo_equipamento
BEFORE INSERT OR UPDATE ON Equipamento
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();


-- MODIFICAÇÃO 2: Função simplificada para apenas realizar a transação de compra
CREATE OR REPLACE FUNCTION comprar_item(
    p_id_estagiario INT,
    p_id_instancia INT,
    p_quantidade INT
) RETURNS TEXT AS $$
DECLARE
    v_item_id INT;
    v_quant_disp INT;
    v_preco INT;
    v_inventario INT;
    v_coins INT;
    v_new_instancia INT;
BEGIN
    SELECT ii.id_item, ii.quantidade, i.preco_base
    INTO v_item_id, v_quant_disp, v_preco
    FROM InstanciaItem ii
    JOIN Item i ON ii.id_item = i.id_item
    WHERE ii.id_instancia = p_id_instancia AND ii.local_atual = 'Loja';

    IF NOT FOUND THEN
        RETURN 'Item não disponível na loja.';
    END IF;

    IF v_quant_disp < p_quantidade THEN
        RETURN 'Quantidade indisponível.';
    END IF;

    SELECT coins INTO v_coins FROM Estagiario WHERE id_personagem = p_id_estagiario;
    IF v_coins < v_preco * p_quantidade THEN
        RETURN 'Moedas insuficientes.';
    END IF;

    SELECT id_inventario INTO v_inventario FROM Inventario WHERE id_estagiario = p_id_estagiario;

    UPDATE Estagiario SET coins = coins - (v_preco * p_quantidade)
    WHERE id_personagem = p_id_estagiario;

    INSERT INTO InstanciaItem(id_item, quantidade, local_atual)
    VALUES (v_item_id, p_quantidade, 'Inventario')
    RETURNING id_instancia INTO v_new_instancia;

    INSERT INTO ItemInventario(id_inventario, id_instancia, quantidade)
    VALUES (v_inventario, v_new_instancia, p_quantidade);

    UPDATE InstanciaItem
    SET quantidade = quantidade - p_quantidade
    WHERE id_instancia = p_id_instancia;
    DELETE FROM InstanciaItem WHERE id_instancia = p_id_instancia AND quantidade <= 0;

    RETURN 'Compra realizada com sucesso!';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Erro inesperado na compra: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION usar_elevador(
    p_id_personagem INT,
    p_andar_destino INT
) RETURNS TEXT AS $$
DECLARE
    v_posicao RECORD;
    v_nova_sala_id INT;
BEGIN
    SELECT * INTO v_posicao
    FROM vw_posicao_estagiario
    WHERE id_personagem = p_id_personagem;

    IF v_posicao.nome_sala != 'Sala Central' THEN
        RETURN 'Você precisa estar na Sala Central para chamar o elevador.';
    END IF;

    SELECT s.id_sala INTO v_nova_sala_id
    FROM Sala s
    JOIN Andar a ON s.id_andar = a.id_andar
    WHERE s.nome = 'Sala Central' AND a.numero = p_andar_destino;

    IF v_nova_sala_id IS NOT NULL THEN
        UPDATE Estagiario
        SET andar_atual = (SELECT id_andar FROM Andar WHERE numero = p_andar_destino),
            sala_atual = v_nova_sala_id
        WHERE id_personagem = p_id_personagem;
        RETURN 'Você chegou ao ' || (SELECT nome FROM Andar WHERE numero = p_andar_destino) || '.';
    ELSE
        RETURN 'Andar de destino inválido.';
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION concluir_missao(
    p_id_estagiario INT,
    p_id_missao INT
) RETURNS TEXT AS $$
DECLARE
    v_missao RECORD;
    v_status_atual VARCHAR(20);
    v_recompensa_texto TEXT;
BEGIN
    SELECT status INTO v_status_atual
    FROM MissaoStatus
    WHERE id_estagiario = p_id_estagiario AND id_missao = p_id_missao;

    IF NOT FOUND THEN
        RETURN 'Erro: Missão não iniciada pelo jogador.';
    END IF;

    IF v_status_atual = 'Concluída' THEN
        RETURN 'Esta missão já foi concluída.';
    END IF;

    SELECT nome, xp_recompensa, moedas_recompensa INTO v_missao
    FROM Missao
    WHERE id_missao = p_id_missao;

    UPDATE Estagiario
    SET xp = xp + v_missao.xp_recompensa,
        coins = coins + v_missao.moedas_recompensa
    WHERE id_personagem = p_id_estagiario;

    UPDATE MissaoStatus
    SET status = 'Concluída'
    WHERE id_estagiario = p_id_estagiario AND id_missao = p_id_missao;

    INSERT INTO MissaoConcluida (id_missao, id_estagiario, xp_ganho, moedas_ganhas)
    VALUES (p_id_missao, p_id_estagiario, v_missao.xp_recompensa, v_missao.moedas_recompensa);

    v_recompensa_texto := 'Missão "' || v_missao.nome || '" concluída! Você ganhou ' || v_missao.xp_recompensa || ' XP e ' || v_missao.moedas_recompensa || ' moedas!';

    RETURN v_recompensa_texto;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Erro inesperado ao concluir a missão: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;


-- =================================================================
-- == MODIFICAÇÃO 3: NOVAS FUNÇÕES PARA INTERAÇÃO COM ITENS ==
-- =================================================================

-- Função para USAR consumíveis e power-ups
CREATE OR REPLACE FUNCTION usar_item(p_id_estagiario INT, p_id_instancia INT)
RETURNS TEXT AS $$
DECLARE
    v_item_record RECORD;
    v_consumivel_record RECORD;
    v_powerup_record RECORD;
BEGIN
    -- Verifica se o item está no inventário do jogador
    SELECT i.id_item, i.nome, i.tipo INTO v_item_record
    FROM ItemInventario ii
    JOIN InstanciaItem inst ON ii.id_instancia = inst.id_instancia
    JOIN Item i ON inst.id_item = i.id_item
    JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
    WHERE inv.id_estagiario = p_id_estagiario AND ii.id_instancia = p_id_instancia;

    IF NOT FOUND THEN
        RETURN 'Item não encontrado no seu inventário.';
    END IF;

    -- Lógica para CONSUMÍVEIS
    IF v_item_record.tipo = 'Consumivel' THEN
        SELECT recuperacao_vida INTO v_consumivel_record FROM Consumivel WHERE id_item = v_item_record.id_item;
        UPDATE Estagiario SET vida = LEAST(100, vida + v_consumivel_record.recuperacao_vida) WHERE id_personagem = p_id_estagiario;

        -- Remove o item do inventário
        DELETE FROM ItemInventario WHERE id_instancia = p_id_instancia;
        DELETE FROM InstanciaItem WHERE id_instancia = p_id_instancia;

        RETURN 'Você usou ' || v_item_record.nome || ' e recuperou ' || v_consumivel_record.recuperacao_vida || ' de vida.';
    END IF;

    -- Lógica para POWER-UPS (NOTA: Efeito aplicado permanentemente por simplicidade)
    IF v_item_record.tipo = 'PowerUp' THEN
        SELECT bonus_ataque INTO v_powerup_record FROM PowerUp WHERE id_item = v_item_record.id_item;
        UPDATE Estagiario SET ataque = ataque + v_powerup_record.bonus_ataque WHERE id_personagem = p_id_estagiario;

        -- Remove o item do inventário
        DELETE FROM ItemInventario WHERE id_instancia = p_id_instancia;
        DELETE FROM InstanciaItem WHERE id_instancia = p_id_instancia;

        RETURN 'Você usou ' || v_item_record.nome || ' e ganhou ' || v_powerup_record.bonus_ataque || ' de ataque permanentemente!';
    END IF;

    RETURN 'Este item não pode ser usado desta forma.';
END;
$$ LANGUAGE plpgsql;

-- Função para EQUIPAR um item
CREATE OR REPLACE FUNCTION equipar_item(p_id_estagiario INT, p_id_instancia INT)
RETURNS TEXT AS $$
DECLARE
    v_equip_record RECORD;
BEGIN
    -- Busca o item e seus atributos
    SELECT i.id_item, i.nome, e.slot, e.bonus_ataque, e.bonus_defesa INTO v_equip_record
    FROM ItemInventario ii
    JOIN InstanciaItem inst ON ii.id_instancia = inst.id_instancia
    JOIN Item i ON inst.id_item = i.id_item
    JOIN Equipamento e ON i.id_item = e.id_item
    JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
    WHERE inv.id_estagiario = p_id_estagiario AND ii.id_instancia = p_id_instancia;

    IF NOT FOUND THEN RETURN 'Item de equipamento não encontrado no inventário.'; END IF;

    -- Verifica se o slot já está ocupado
    IF EXISTS (SELECT 1 FROM EstagiarioEquipamento WHERE id_estagiario = p_id_estagiario AND slot = v_equip_record.slot) THEN
        RETURN 'Slot "' || v_equip_record.slot || '" já está ocupado. Desequipe o item atual primeiro.';
    END IF;

    -- Aplica os bônus
    UPDATE Estagiario
    SET ataque = ataque + v_equip_record.bonus_ataque,
        defesa = defesa + v_equip_record.bonus_defesa
    WHERE id_personagem = p_id_estagiario;

    -- Move o item do inventário para a tabela de equipamentos
    DELETE FROM ItemInventario WHERE id_instancia = p_id_instancia;
    INSERT INTO EstagiarioEquipamento (id_estagiario, id_instancia, slot)
    VALUES (p_id_estagiario, p_id_instancia, v_equip_record.slot);

    RETURN v_equip_record.nome || ' equipado com sucesso!';
END;
$$ LANGUAGE plpgsql;

-- Função para DESEQUIPAR um item
CREATE OR REPLACE FUNCTION desequipar_item(p_id_estagiario INT, p_id_instancia INT)
RETURNS TEXT AS $$
DECLARE
    v_equip_record RECORD;
    v_id_inventario INT;
BEGIN
    -- Busca o item equipado e seus atributos
    SELECT i.id_item, i.nome, e.slot, e.bonus_ataque, e.bonus_defesa INTO v_equip_record
    FROM EstagiarioEquipamento ee
    JOIN InstanciaItem inst ON ee.id_instancia = inst.id_instancia
    JOIN Item i ON inst.id_item = i.id_item
    JOIN Equipamento e ON i.id_item = e.id_item
    WHERE ee.id_estagiario = p_id_estagiario AND ee.id_instancia = p_id_instancia;

    IF NOT FOUND THEN RETURN 'Você não está equipando este item.'; END IF;

    -- Remove os bônus
    UPDATE Estagiario
    SET ataque = ataque - v_equip_record.bonus_ataque,
        defesa = defesa - v_equip_record.bonus_defesa
    WHERE id_personagem = p_id_estagiario;

    -- Move o item da tabela de equipamentos de volta para o inventário
    SELECT id_inventario INTO v_id_inventario FROM Inventario WHERE id_estagiario = p_id_estagiario;
    DELETE FROM EstagiarioEquipamento WHERE id_instancia = p_id_instancia;
    INSERT INTO ItemInventario (id_inventario, id_instancia, quantidade) VALUES (v_id_inventario, p_id_instancia, 1);

    RETURN v_equip_record.nome || ' desequipado e guardado na mochila.';
END;
$$ LANGUAGE plpgsql;