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

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION criar_inventario_e_arma()
RETURNS TRIGGER AS $$
DECLARE
    v_id_inventario INT;
    v_id_item INT;
    v_id_instancia INT;
BEGIN
    -- Cria o inventário
    INSERT INTO Inventario (id_estagiario, espaco_total)
    VALUES (NEW.id_personagem, 12)
    RETURNING id_inventario INTO v_id_inventario;

    -- Pega o id do item 'Livro básico de sql'
    SELECT id_item INTO v_id_item 
    FROM Item 
    WHERE nome = 'Livro básico de sql' 
    LIMIT 1;

    IF v_id_item IS NULL THEN
        RAISE EXCEPTION 'Não foi encontrado o item inicial "Livro básico de sql".';
    END IF;

    -- Cria uma instância do item, vinculando ao estagiário
    INSERT INTO InstanciaItem (id_item, quantidade, local_atual, id_estagiario)
    VALUES (v_id_item, 1, 'Inventario', NEW.id_personagem)
    RETURNING id_instancia INTO v_id_instancia;

    -- Insere a instância no inventário
    INSERT INTO ItemInventario (id_inventario, id_instancia)
    VALUES (v_id_inventario, v_id_instancia);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_criar_inventario ON Estagiario;
DROP TRIGGER IF EXISTS trigger_adicionar_armas_inventario ON Estagiario;

CREATE TRIGGER trigger_criar_inventario_e_arma
AFTER INSERT ON Estagiario
FOR EACH ROW
EXECUTE FUNCTION criar_inventario_e_arma();


CREATE OR REPLACE FUNCTION inserir_missoes_iniciais()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
    SELECT id_missao, NEW.id_personagem, 'Disponível'
    FROM Missao;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_inserir_missoes_iniciais
AFTER INSERT ON Estagiario
FOR EACH ROW
EXECUTE FUNCTION inserir_missoes_iniciais();

