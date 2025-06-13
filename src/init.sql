-- BOA PRÁTICA: Usamos 'ADD COLUMN IF NOT EXISTS' para evitar erros se o script rodar mais de uma vez.
ALTER TABLE SBD1.Personagem
ADD COLUMN IF NOT EXISTS id_sala_atual INT;

-- Adicionamos a constraint separadamente para garantir que a coluna exista primeiro.
ALTER TABLE SBD1.Personagem
ADD CONSTRAINT fk_sala_atual
    FOREIGN KEY(id_sala_atual)
    REFERENCES SBD1.Sala(id);

-- Função para criar um novo personagem.
-- OBSERVAÇÃO: Para a exceção de nome duplicado funcionar, sua tabela Personagem
-- precisa ter uma constraint UNIQUE no campo 'nome'. Ex:
-- ALTER TABLE SBD1.Personagem ADD CONSTRAINT UQ_Personagem_Nome UNIQUE(nome);
CREATE OR REPLACE FUNCTION SBD1.criar_personagem(
    p_nome_personagem VARCHAR(100) -- BOA PRÁTICA: 'p_' para parâmetros
) RETURNS TEXT AS $$
DECLARE
    v_mensagem TEXT; -- BOA PRÁTICA: 'v_' para variáveis
BEGIN
    INSERT INTO SBD1.Personagem(nome, id_sala_atual)
    VALUES (p_nome_personagem, 1) -- ID 1 continua sendo a Recepção
    RETURNING 'Personagem "' || p_nome_personagem || '" criado com sucesso!' INTO v_mensagem;

    RETURN v_mensagem;
EXCEPTION
    WHEN unique_violation THEN
        RETURN 'Erro: Já existe um personagem com este nome.';
    WHEN OTHERS THEN
        RETURN 'Erro inesperado ao criar personagem.';
END;
$$ LANGUAGE plpgsql;


-- Função para obter a descrição completa do local atual do personagem.
CREATE OR REPLACE FUNCTION SBD1.descrever_local_atual(
    p_id_personagem INT -- BOA PRÁTICA: 'p_' para parâmetros
) RETURNS TEXT AS $$
DECLARE
    -- CORREÇÃO CRÍTICA: Renomeamos as variáveis para não conflitarem com nomes de colunas.
    v_descricao_sala TEXT;
    v_nome_sala_atual VARCHAR(100);
    v_saidas_disponiveis TEXT;
    v_id_sala_atual INT;
BEGIN
    -- Encontra a sala atual do personagem
    SELECT P.id_sala_atual INTO v_id_sala_atual
    FROM SBD1.Personagem P
    WHERE P.id = p_id_personagem;

    -- Se, por algum motivo, o personagem não tiver uma localização, retorne um erro.
    IF v_id_sala_atual IS NULL THEN
        RETURN 'Erro: Personagem não encontrado ou sem localização definida.';
    END IF;

    -- Pega os detalhes da sala
    SELECT S.nome, S.descricao INTO v_nome_sala_atual, v_descricao_sala
    FROM SBD1.Sala S
    WHERE S.id = v_id_sala_atual;

    -- Monta a lista de saídas
    SELECT string_agg(C.nome_saida, ', ') INTO v_saidas_disponiveis
    FROM SBD1.Conexao C
    WHERE C.id_sala_origem = v_id_sala_atual;

    IF v_saidas_disponiveis IS NULL THEN
        v_saidas_disponiveis := 'Nenhuma';
    END IF;

    -- Monta a descrição final
    RETURN 'Você está em: ' || v_nome_sala_atual || E'\n' ||
           v_descricao_sala || E'\n\n' ||
           'Saídas disponíveis: ' || v_saidas_disponiveis;
END;
$$ LANGUAGE plpgsql;


-- A função mais importante: Mover o personagem.
CREATE OR REPLACE FUNCTION SBD1.mover_personagem(
    p_id_personagem INT,         -- BOA PRÁTICA: 'p_' para parâmetros
    p_direcao_movimento VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    -- CORREÇÃO CRÍTICA: Renomeamos as variáveis para evitar o bug de comparação.
    v_id_sala_destino INT;
    v_id_sala_origem INT;
BEGIN
    -- Pega a localização atual do personagem
    SELECT P.id_sala_atual INTO v_id_sala_origem
    FROM SBD1.Personagem P
    WHERE P.id = p_id_personagem;

    -- Tenta encontrar uma conexão válida a partir da sala atual com o nome da direção
    -- CORREÇÃO CRÍTICA: A comparação agora é entre a coluna da tabela (C.id_sala_origem)
    -- e a nossa variável que guarda a localização do personagem (v_id_sala_origem).
    SELECT C.id_sala_destino INTO v_id_sala_destino
    FROM SBD1.Conexao C
    WHERE C.id_sala_origem = v_id_sala_origem -- AQUI ESTAVA O BUG
      AND lower(C.nome_saida) = lower(p_direcao_movimento);

    -- Se encontrou um destino, atualiza a localização do personagem
    IF v_id_sala_destino IS NOT NULL THEN
        UPDATE SBD1.Personagem
        SET id_sala_atual = v_id_sala_destino
        WHERE id = p_id_personagem;

        -- Retorna a descrição do novo local
        RETURN SBD1.descrever_local_atual(p_id_personagem);
    ELSE
        -- Se não encontrou, retorna uma mensagem de erro
        RETURN 'Você não pode ir por aí.';
    END IF;
END;
$$ LANGUAGE plpgsql;