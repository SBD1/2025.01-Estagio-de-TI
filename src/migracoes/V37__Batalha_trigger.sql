CREATE OR REPLACE FUNCTION criar_instancia_estagiario_batalha()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO InstanciaEstagiario (id_personagem, vida_atual, status, id_batalha)
    VALUES (NEW.id_personagem, 1000, 'Normal', NEW.id_batalha);  -- exemplo: vida inicial 100

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_criar_instancia_estagiario
AFTER INSERT ON Batalha
FOR EACH ROW
EXECUTE FUNCTION criar_instancia_estagiario_batalha();



CREATE OR REPLACE FUNCTION deletar_instancia_estagiario_batalha()
RETURNS TRIGGER AS $$
BEGIN
    -- Só deleta se o resultado for preenchido (não NULL)
    IF NEW.resultado IS NOT NULL THEN
        DELETE FROM InstanciaEstagiario WHERE id_batalha = NEW.id_batalha;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_deletar_instancia_estagiario
AFTER UPDATE ON Batalha
FOR EACH ROW
WHEN (OLD.resultado IS NULL AND NEW.resultado IS NOT NULL)
EXECUTE FUNCTION deletar_instancia_estagiario_batalha();


