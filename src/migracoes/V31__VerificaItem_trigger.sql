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
