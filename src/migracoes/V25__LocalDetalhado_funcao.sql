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