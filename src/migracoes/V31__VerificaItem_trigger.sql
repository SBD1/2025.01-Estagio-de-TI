CREATE OR REPLACE FUNCTION verificar_campos_por_tipo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.tipo = 'PowerUp' THEN
        IF NEW.recuperacao_vida IS NOT NULL OR NEW.dano IS NOT NULL THEN
            RAISE EXCEPTION 'Item tipo PowerUp não pode ter campos de outros tipos preenchidos.';
        END IF;
        
    ELSIF NEW.tipo = 'Consumivel' THEN
        IF NEW.bonus_ataque IS NOT NULL OR NEW.dano IS NOT NULL THEN
            RAISE EXCEPTION 'Item tipo Consumivel não pode ter campos de outros tipos preenchidos.';
        END IF;

    ELSIF NEW.tipo = 'Arma' THEN
        IF NEW.recuperacao_vida IS NOT NULL OR NEW.bonus_ataque IS NOT NULL THEN
            RAISE EXCEPTION 'Item tipo Arma não pode ter campos de outros tipos preenchidos.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificar_campos_item
BEFORE INSERT OR UPDATE ON Item
FOR EACH ROW
EXECUTE FUNCTION verificar_campos_por_tipo();
