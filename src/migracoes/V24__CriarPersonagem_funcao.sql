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
        status,
        andar_atual,
        sala_atual
    ) VALUES (
        p_nome_personagem,
        0,      
        1,    
        50,    
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

