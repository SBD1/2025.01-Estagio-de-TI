CREATE FUNCTION mover_personagem(
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


CREATE FUNCTION pegar_respeito(p_id_personagem INT) RETURNS INT AS $$
DECLARE
    v_respeito INT;
BEGIN
    SELECT respeito
    INTO v_respeito
    FROM Estagiario
    WHERE id_personagem = p_id_personagem;

    RETURN v_respeito;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION diminuir_respeito(
    p_id_personagem INT,
    p_valor INT
) RETURNS VOID AS $$
BEGIN
    UPDATE Estagiario
    SET respeito = GREATEST(respeito - p_valor, 0)
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION verificar_respeito_minimo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.respeito < 5 THEN
        RAISE NOTICE 'Você perdeu o jogo! Seu respeito caiu abaixo de 5.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_verificar_respeito ON Estagiario;

CREATE TRIGGER trigger_verificar_respeito
BEFORE UPDATE ON Estagiario
FOR EACH ROW
EXECUTE FUNCTION verificar_respeito_minimo();


CREATE FUNCTION pode_conversar_com_npc(p_id_estagiario INT, p_id_npc INT)
RETURNS BOOLEAN AS $$
DECLARE
    v_respeito_estagiario INT;
    v_respeito_npc INT;
BEGIN
    SELECT respeito INTO v_respeito_estagiario FROM Estagiario WHERE id_personagem = p_id_estagiario;
    SELECT respeito_personagem INTO v_respeito_npc FROM NPC WHERE id_npc = p_id_npc;

    IF v_respeito_estagiario >= v_respeito_npc THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION verificar_e_atualizar_nivel()
RETURNS TRIGGER AS $$
BEGIN
    --só roda se xp aumentar
    IF NEW.xp > OLD.xp THEN
        IF NEW.xp >= 1000 AND NEW.nivel < 5 THEN
            NEW.nivel := 5;
        ELSIF NEW.xp >= 350 AND NEW.nivel < 4 THEN
            NEW.nivel := 4;
        ELSIF NEW.xp >= 200 AND NEW.nivel < 3 THEN
            NEW.nivel := 3;
        ELSIF NEW.xp >= 50 AND NEW.nivel < 2 THEN
            NEW.nivel := 2;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualizar_nivel
BEFORE UPDATE ON Estagiario
FOR EACH ROW
WHEN (NEW.xp IS DISTINCT FROM OLD.xp)
EXECUTE FUNCTION verificar_e_atualizar_nivel();


CREATE OR REPLACE FUNCTION desbloquear_ataques_por_livro()
RETURNS TRIGGER AS $$
DECLARE
    v_id_personagem INT;
    v_nome_item TEXT;
BEGIN
    IF NEW.lido IS TRUE AND OLD.lido IS DISTINCT FROM TRUE THEN
        -- Dono da instância
        SELECT id_estagiario INTO v_id_personagem
        FROM InstanciaItem
        WHERE id_instancia = NEW.id_instancia;

        -- Nome do item lido
        SELECT i.nome INTO v_nome_item
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        WHERE ii.id_instancia = NEW.id_instancia;

        RAISE NOTICE 'Livro lido: %, personagem: %', v_nome_item, v_id_personagem;

        -- Comparação por nome, ignorando caixa
        IF v_nome_item ILIKE 'livro básico de sql' THEN
            INSERT INTO PersonagemAtaque (id_personagem, id_ataque) VALUES
                (v_id_personagem, 1),
                (v_id_personagem, 2),
                (v_id_personagem, 3)
            ON CONFLICT DO NOTHING;

        ELSIF v_nome_item ILIKE 'livro avançado de sql' THEN
            INSERT INTO PersonagemAtaque (id_personagem, id_ataque) VALUES
                (v_id_personagem, 5),
                (v_id_personagem, 12),
                (v_id_personagem, 14)
            ON CONFLICT DO NOTHING;

        ELSIF v_nome_item ILIKE 'guia definitivo de depuração' THEN
            INSERT INTO PersonagemAtaque (id_personagem, id_ataque) VALUES
                (v_id_personagem, 1),
                (v_id_personagem, 17),
                (v_id_personagem, 13)
            ON CONFLICT DO NOTHING;

        ELSIF v_nome_item ILIKE 'manual de defesa digital' THEN
            INSERT INTO PersonagemAtaque (id_personagem, id_ataque) VALUES
                (v_id_personagem, 6),
                (v_id_personagem, 9),
                (v_id_personagem, 12)
            ON CONFLICT DO NOTHING;

        ELSIF v_nome_item ILIKE 'livro do senai' THEN
            INSERT INTO PersonagemAtaque (id_personagem, id_ataque) VALUES
                (v_id_personagem, 4),
                (v_id_personagem, 10),
                (v_id_personagem, 11),
                (v_id_personagem, 18)
            ON CONFLICT DO NOTHING;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_ler_livro ON InstanciaItem;

CREATE TRIGGER trigger_ler_livro
AFTER UPDATE OF lido ON InstanciaItem
FOR EACH ROW
WHEN (NEW.lido = TRUE)
EXECUTE FUNCTION desbloquear_ataques_por_livro();

