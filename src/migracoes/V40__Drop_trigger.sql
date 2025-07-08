CREATE OR REPLACE FUNCTION aplicar_recompensas()
RETURNS TRIGGER AS $$
DECLARE
    inimigo_id INT;
    item_id INT;
    chance REAL;
    drop_reg RECORD;
    qtd_inimigos INT;
BEGIN
    --aplica se for vitória
    IF NEW.resultado <> 'Vitória' THEN
        RETURN NEW;
    END IF;

    --recompensa básica
    UPDATE Estagiario
    SET xp = xp + 10,
        respeito = respeito + 5,
        dinheiro = dinheiro + 20
    WHERE id_personagem = NEW.id_personagem;

    --dropar itens com base nos inimigos mortos
    FOR drop_reg IN
        SELECT ii.id_inimigo, di.id_item, di.chance_drop
        FROM BatalhaInimigos bi
        JOIN InstanciaInimigo ii ON bi.id_inimigo = ii.id_instancia
        JOIN DropInimigo di ON ii.id_inimigo = di.id_inimigo
        WHERE bi.id_batalha = NEW.id_batalha
    LOOP
        IF random() < drop_reg.chance_drop THEN

            INSERT INTO InstanciaItem (id_personagem, id_item, quantidade)
            VALUES (NEW.id_personagem, drop_reg.id_item, 1)
            ON CONFLICT (id_personagem, id_item) DO UPDATE
            SET quantidade = InstanciaItem.quantidade + 1;
        END IF;
    END LOOP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION processar_drops_missao(p_id_estagiario INT, p_id_missao INT) RETURNS VOID AS $$
DECLARE
    drop_row RECORD;
BEGIN
    FOR drop_row IN 
        SELECT id_item, chance FROM MissaoDrop WHERE id_missao = p_id_missao
    LOOP
        IF random() <= drop_row.chance THEN
            INSERT INTO InstanciaItem(id_item, id_estagiario, quantidade)
            VALUES (drop_row.id_item, p_id_estagiario, 1)
            ON CONFLICT (id_item, id_estagiario) DO UPDATE
                SET quantidade = InstanciaItem.quantidade + 1;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION trigger_drop_missao() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Concluída' AND OLD.status != 'Concluída' THEN
        PERFORM processar_drops_missao(NEW.id_estagiario, NEW.id_missao);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_drop_missao
AFTER UPDATE ON MissaoStatus
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE FUNCTION trigger_drop_missao();
