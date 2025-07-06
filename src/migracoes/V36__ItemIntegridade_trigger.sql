CREATE OR REPLACE FUNCTION validar_item_tipo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tipo = 'Arma' THEN
        IF NEW.dano IS NULL THEN
            RAISE EXCEPTION 'Armas devem ter o campo "dano" preenchido.';
        END IF;
        IF NEW.recuperacao_vida IS NOT NULL OR NEW.bonus_ataque IS NOT NULL THEN
            RAISE EXCEPTION 'Armas não devem ter "recuperacao_vida" ou "bonus_ataque".';
        END IF;

    ELSIF NEW.tipo = 'Consumivel' THEN
        IF NEW.recuperacao_vida IS NULL THEN
            RAISE EXCEPTION 'Consumíveis devem ter o campo "recuperacao_vida" preenchido.';
        END IF;
        IF NEW.dano IS NOT NULL OR NEW.bonus_ataque IS NOT NULL THEN
            RAISE EXCEPTION 'Consumíveis não devem ter "dano" ou "bonus_ataque".';
        END IF;

    ELSIF NEW.tipo = 'PowerUp' THEN
        IF NEW.bonus_ataque IS NULL THEN
            RAISE EXCEPTION 'PowerUps devem ter o campo "bonus_ataque" preenchido.';
        END IF;
        IF NEW.dano IS NOT NULL OR NEW.recuperacao_vida IS NOT NULL THEN
            RAISE EXCEPTION 'PowerUps não devem ter "dano" ou "recuperacao_vida".';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_validar_item_tipo ON Item;

CREATE TRIGGER trigger_validar_item_tipo
BEFORE INSERT OR UPDATE ON Item
FOR EACH ROW
EXECUTE FUNCTION validar_item_tipo();
