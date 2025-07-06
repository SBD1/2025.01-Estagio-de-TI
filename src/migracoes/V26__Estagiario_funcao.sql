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


CREATE OR REPLACE FUNCTION pegar_respeito(p_id_personagem INT) RETURNS INT AS $$
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

CREATE OR REPLACE FUNCTION verificar_respeito_minimo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.respeito < 5 THEN
        RAISE EXCEPTION 'Você perdeu o jogo! Seu respeito caiu abaixo de 5.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_verificar_respeito ON Estagiario;

CREATE TRIGGER trigger_verificar_respeito
BEFORE UPDATE OF respeito ON Estagiario
FOR EACH ROW
EXECUTE FUNCTION verificar_respeito_minimo();


CREATE OR REPLACE FUNCTION pode_conversar_com_npc(p_id_estagiario INT, p_id_npc INT)
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