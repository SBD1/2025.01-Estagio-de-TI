-- Adiciona uma coluna para saber onde o personagem está.
-- Usamos o ID da sala para rastrear a localização.
ALTER TABLE SBD1.Personagem
ADD COLUMN id_sala_atual INT,
ADD CONSTRAINT fk_sala_atual
    FOREIGN KEY(id_sala_atual)
    REFERENCES SBD1.Sala(id);

-- Função para criar um novo personagem.
-- Ele sempre começará na "Recepção" (Sala de id=1 no 1º Andar).
CREATE OR REPLACE FUNCTION SBD1.criar_personagem(
    nome_personagem VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    novo_id INT;
    mensagem TEXT;
BEGIN
    -- Insere o novo personagem
    INSERT INTO SBD1.Personagem(nome, id_sala_atual)
    VALUES (nome_personagem, 1) -- ID 1 é a Recepção
    RETURNING id INTO novo_id;

    mensagem := 'Personagem "' || nome_personagem || '" criado com sucesso!';
    RETURN mensagem;
EXCEPTION
    WHEN unique_violation THEN
        RETURN 'Erro: Já existe um personagem com este nome.';
    WHEN OTHERS THEN
        RETURN 'Erro inesperado ao criar personagem.';
END;
$$ LANGUAGE plpgsql;


-- Função para obter a descrição completa do local atual do personagem.
-- Retorna o nome da sala, descrição e as saídas disponíveis.
CREATE OR REPLACE FUNCTION SBD1.descrever_local_atual(
    id_personagem_atual INT
) RETURNS TEXT AS $$
DECLARE
    descricao_sala TEXT;
    nome_sala_atual VARCHAR(100);
    saidas_disponiveis TEXT;
    id_sala_atual INT;
BEGIN
    -- Encontra a sala atual do personagem
    SELECT P.id_sala_atual INTO id_sala_atual
    FROM SBD1.Personagem P
    WHERE P.id = id_personagem_atual;

    -- Pega os detalhes da sala
    SELECT nome, descricao INTO nome_sala_atual, descricao_sala
    FROM SBD1.Sala
    WHERE id = id_sala_atual;

    -- Monta a lista de saídas
    SELECT string_agg(C.nome_saida, ', ') INTO saidas_disponiveis
    FROM SBD1.Conexao C
    WHERE C.id_sala_origem = id_sala_atual;

    IF saidas_disponiveis IS NULL THEN
        saidas_disponiveis := 'Nenhuma';
    END IF;

    -- Monta a descrição final
    RETURN 'Você está em: ' || nome_sala_atual || E'\n' ||
           descricao_sala || E'\n\n' ||
           'Saídas disponíveis: ' || saidas_disponiveis;
END;
$$ LANGUAGE plpgsql;


-- A função mais importante: Mover o personagem.
CREATE OR REPLACE FUNCTION SBD1.mover_personagem(
    id_personagem_atual INT,
    direcao_movimento VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    id_sala_destino INT;
    id_sala_origem INT;
    mensagem TEXT;
BEGIN
    -- Pega a localização atual do personagem
    SELECT id_sala_atual INTO id_sala_origem
    FROM SBD1.Personagem
    WHERE id = id_personagem_atual;

    -- Tenta encontrar uma conexão válida a partir da sala atual com o nome da direção
    SELECT C.id_sala_destino INTO id_sala_destino
    FROM SBD1.Conexao C
    WHERE C.id_sala_origem = id_sala_origem
      AND lower(C.nome_saida) = lower(direcao_movimento);

    -- Se encontrou um destino, atualiza a localização do personagem
    IF id_sala_destino IS NOT NULL THEN
        UPDATE SBD1.Personagem
        SET id_sala_atual = id_sala_destino
        WHERE id = id_personagem_atual;

        -- Retorna a descrição do novo local
        RETURN SBD1.descrever_local_atual(id_personagem_atual);
    ELSE
        -- Se não encontrou, retorna uma mensagem de erro
        RETURN 'Você não pode ir por aí.';
    END IF;
END;
$$ LANGUAGE plpgsql;