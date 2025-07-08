CREATE OR REPLACE FUNCTION atualizar_localizacao_item()
RETURNS TRIGGER AS $$
BEGIN
    -- Limpa o item de todas as tabelas auxiliares para evitar duplicidade
    DELETE FROM ItemInventario WHERE id_instancia = NEW.id_instancia;
    DELETE FROM ItemNoChao WHERE id_instancia = NEW.id_instancia;
    DELETE FROM ItemNpc WHERE id_instancia = NEW.id_instancia;

    IF NEW.local_atual = 'Inventario' THEN
        IF NEW.id_estagiario IS NULL THEN
            RETURN NEW;
        END IF;

        -- Busca o id_inventario do estagiário (dono)
        INSERT INTO ItemInventario (id_inventario, id_instancia, quantidade)
        SELECT inv.id_inventario, NEW.id_instancia, NEW.quantidade
        FROM Inventario inv
        WHERE inv.id_estagiario = NEW.id_estagiario;

    ELSIF NEW.local_atual = 'Chao' THEN
        IF NEW.id_sala IS NULL THEN
            RAISE EXCEPTION 'id_sala não pode ser NULL quando local_atual = Chao';
        END IF;

        INSERT INTO ItemNoChao (id_instancia, id_sala)
        VALUES (NEW.id_instancia, NEW.id_sala);

    ELSIF NEW.local_atual = 'Npc' THEN
        IF NEW.id_npc IS NULL THEN
            RAISE EXCEPTION 'id_npc não pode ser NULL quando local_atual = Npc';
        END IF;

        INSERT INTO ItemNpc (id_instancia, id_npc)
        VALUES (NEW.id_instancia, NEW.id_npc);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_atualizar_localizacao_item ON InstanciaItem;

CREATE TRIGGER trg_atualizar_localizacao_item
AFTER INSERT OR UPDATE ON InstanciaItem
FOR EACH ROW
EXECUTE FUNCTION atualizar_localizacao_item();

