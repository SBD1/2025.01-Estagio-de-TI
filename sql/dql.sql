CREATE OR REPLACE FUNCTION criar_personagem(
    p_nome_personagem VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_sala_inicial RECORD;
    v_id_estagiario INT;
BEGIN

    SELECT id_sala, id_andar INTO v_sala_inicial
    FROM vw_sala_central --uma view
    WHERE numero_andar = 0;

    INSERT INTO Estagiario(
        nome,
        xp,
        nivel,
        respeito,
        coins,
        ataque,
        defesa,
        vida,
        status,
        andar_atual,
        sala_atual
    ) VALUES (
        p_nome_personagem,
        0,
        1,
        50,
        100,
        10,
        5,
        100,
        'Normal',
        v_sala_inicial.id_andar,
        v_sala_inicial.id_sala
    ) RETURNING id_personagem INTO v_id_estagiario;

    RETURN 'Estagiário "' || p_nome_personagem || '" criado com sucesso! (ID: ' || v_id_estagiario || ')';

EXCEPTION
    WHEN unique_violation THEN
        RETURN 'Erro: Já existe um estagiário com este nome.';
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
    FROM vw_posicao_estagiario --uma view
    WHERE id_personagem = p_id_personagem;

    RETURN QUERY
    WITH saidas_possiveis AS (
        
        SELECT 'Ir para ' || nome_sala_destino as direcao
        FROM vw_conexoes_salas
        WHERE id_sala_origem = v_posicao.sala_atual

        UNION ALL

     
        SELECT 
            CASE 
                WHEN a.numero > v_posicao.numero_andar THEN 'Subir para ' || REGEXP_REPLACE(a.nome, '.*?: ', '')
                WHEN a.numero < v_posicao.numero_andar THEN 'Descer para ' || REGEXP_REPLACE(a.nome, '.*?: ', '')
            END
        FROM Andar a
        WHERE v_posicao.nome_sala = 'Sala Central'
        AND ((a.numero = v_posicao.numero_andar + 1 AND v_posicao.numero_andar < 10)
          OR (a.numero = v_posicao.numero_andar - 1 AND v_posicao.numero_andar > -2))
    )
    SELECT 
        (v_posicao.nome_andar || E'\nSala: ' || v_posicao.nome_sala),
        v_posicao.descricao_sala,
        ARRAY(
            SELECT direcao 
            FROM saidas_possiveis 
            WHERE direcao IS NOT NULL
            ORDER BY direcao
        ); -- esse text é para transformar em um vetor as saidas
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION mover_personagem(
    p_id_personagem INT,
    p_direcao_texto VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_posicao RECORD;
    v_novo_andar INT;
    v_nova_sala INT;
BEGIN

    SELECT * INTO v_posicao
    FROM vw_posicao_estagiario --uma view
    WHERE id_personagem = p_id_personagem;

    IF (p_direcao_texto LIKE 'Subir para%' OR p_direcao_texto LIKE 'Descer para%') THEN

        IF v_posicao.nome_sala != 'Sala Central' THEN
            RETURN 'Você só pode mudar de andar a partir da Sala Central.';
        END IF;


        SELECT sc.id_andar, sc.id_sala 
        INTO v_novo_andar, v_nova_sala
        FROM vw_sala_central sc
        JOIN Andar a ON sc.id_andar = a.id_andar
        WHERE p_direcao_texto LIKE '%' || REGEXP_REPLACE(a.nome, '.*?: ', '');

        IF v_novo_andar IS NOT NULL THEN
            UPDATE Estagiario 
            SET andar_atual = v_novo_andar,
                sala_atual = v_nova_sala
            WHERE id_personagem = p_id_personagem;
            
            RETURN 'Você mudou de andar.';
        END IF;

    ELSIF p_direcao_texto LIKE 'Ir para%' THEN

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

-- PowerUp
CREATE TRIGGER validar_tipo_powerup
BEFORE INSERT OR UPDATE ON PowerUp
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();

-- Consumivel
CREATE TRIGGER validar_tipo_consumivel
BEFORE INSERT OR UPDATE ON Consumivel
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();

-- Equipamento
CREATE TRIGGER validar_tipo_equipamento
BEFORE INSERT OR UPDATE ON Equipamento
FOR EACH ROW
EXECUTE FUNCTION verificar_item_tipo_unico();


--
-- Procedimento para comprar item na loja
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
    v_tipo TEXT;
    v_bonus INT;
BEGIN
    SELECT ii.id_item, ii.quantidade, i.preco_base
    INTO v_item_id, v_quant_disp, v_preco
    FROM InstanciaItem ii
    JOIN Item i ON ii.id_item = i.id_item
    WHERE ii.id_instancia = p_id_instancia AND ii.local_atual = 'Loja';

    IF NOT FOUND THEN
        RETURN 'Item nao disponivel na loja.';
    END IF;

    IF v_quant_disp < p_quantidade THEN
        RETURN 'Quantidade indisponivel.';
    END IF;

    SELECT coins INTO v_coins FROM Estagiario WHERE id_personagem = p_id_estagiario;
    IF v_coins < v_preco * p_quantidade THEN
        RETURN 'Moedas insuficientes.';
    END IF;

    SELECT id_inventario INTO v_inventario FROM Inventario WHERE id_estagiario = p_id_estagiario;

    UPDATE Estagiario SET coins = coins - v_preco * p_quantidade
    WHERE id_personagem = p_id_estagiario;

    INSERT INTO InstanciaItem(id_item, quantidade, local_atual)
    VALUES (v_item_id, p_quantidade, 'Inventario')
    RETURNING id_instancia INTO v_new_instancia;

    INSERT INTO ItemInventario(id_inventario, id_instancia, quantidade)
    VALUES (v_inventario, v_new_instancia, p_quantidade);

    -- Aplica bonus do item nas caracteristicas do jogador
    SELECT tipo INTO v_tipo FROM Item WHERE id_item = v_item_id;

    IF v_tipo = 'PowerUp' THEN
        SELECT bonus_ataque INTO v_bonus FROM PowerUp WHERE id_item = v_item_id;
        UPDATE Estagiario SET ataque = ataque + v_bonus * p_quantidade
        WHERE id_personagem = p_id_estagiario;
    ELSIF v_tipo = 'Consumivel' THEN
        SELECT recuperacao_vida INTO v_bonus FROM Consumivel WHERE id_item = v_item_id;
        UPDATE Estagiario SET vida = LEAST(vida + v_bonus * p_quantidade, 100)
        WHERE id_personagem = p_id_estagiario;
    ELSIF v_tipo = 'Equipamento' THEN
        SELECT bonus_permanente INTO v_bonus FROM Equipamento WHERE id_item = v_item_id;
        UPDATE Estagiario SET ataque = ataque + v_bonus * p_quantidade
        WHERE id_personagem = p_id_estagiario;
    END IF;

    UPDATE InstanciaItem
    SET quantidade = quantidade - p_quantidade
    WHERE id_instancia = p_id_instancia;
    DELETE FROM InstanciaItem WHERE id_instancia = p_id_instancia AND quantidade <= 0;

    RETURN 'Compra realizada com sucesso.';
END;
$$ LANGUAGE plpgsql;
