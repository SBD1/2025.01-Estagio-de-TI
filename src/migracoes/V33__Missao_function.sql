CREATE OR REPLACE FUNCTION dialogo_supervisor(
    p_id_npc INT,
    p_id_estagiario INT
) RETURNS TEXT AS $$
DECLARE
    v_id_missao INT;
    v_status TEXT;
    v_nome_missao TEXT;
BEGIN
    -- Busca missão principal desse supervisor para o estagiário
    SELECT m.id_missao, m.nome
      INTO v_id_missao, v_nome_missao
      FROM Missao m
     WHERE m.id_supervisor = p_id_npc
     LIMIT 1;

    IF v_id_missao IS NULL THEN
        RETURN 'Não tenho missões para você no momento.';
    END IF;

    -- Verifica status da missão para o estagiário
    SELECT status INTO v_status
      FROM MissaoStatus
     WHERE id_missao = v_id_missao AND id_estagiario = p_id_estagiario;

    IF v_status = 'Disponível' THEN
        RETURN 'Tenho uma missão para você: ' || v_nome_missao || '. Deseja aceitar?';
    ELSIF v_status = 'Em andamento' THEN
        RETURN 'Termine a sua missão: : ' || v_nome_missao || '. Vá cumprir!';
    ELSIF v_status = 'Concluída' THEN
        RETURN 'Parabéns por concluir a missão: ' || v_nome_missao || '!, não tenho mais nada a dizer';
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION aceitar_missao(
    p_id_missao INT,
    p_id_estagiario INT
) RETURNS TEXT AS $$
BEGIN
    INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
    VALUES (p_id_missao, p_id_estagiario, 'Em andamento')
    ON CONFLICT (id_missao, id_estagiario) DO NOTHING;
    RETURN 'Missão aceita!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION concluir_missao(
    p_id_missao INT,
    p_id_estagiario INT
) RETURNS TEXT AS $$
BEGIN
    UPDATE MissaoStatus
       SET status = 'Concluída'
     WHERE id_missao = p_id_missao AND id_estagiario = p_id_estagiario;
    RETURN 'Missão concluída!';
END;
$$ LANGUAGE plpgsql;