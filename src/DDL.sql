-- Cria o Schema para organizar todos os objetos do nosso jogo
CREATE SCHEMA IF NOT EXISTS SBD1;

-- Criação das Tabelas com o prefixo do Schema
CREATE TABLE SBD1.Andar (
    id SERIAL PRIMARY KEY,
    numero INT NOT NULL,
    descricao VARCHAR(255)
);

CREATE TABLE SBD1.Sala (
    id SERIAL PRIMARY KEY,
    id_andar INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    FOREIGN KEY (id_andar) REFERENCES SBD1.Andar(id)
);

CREATE TABLE SBD1.Personagem (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_sala_atual INT,
    CONSTRAINT UQ_Personagem_Nome UNIQUE(nome), -- Constraint para evitar nomes duplicados
    FOREIGN KEY (id_sala_atual) REFERENCES SBD1.Sala(id)
);

CREATE TABLE SBD1.Conexao (
    id SERIAL PRIMARY KEY,
    id_sala_origem INT NOT NULL,
    id_sala_destino INT NOT NULL,
    nome_saida VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_sala_origem) REFERENCES SBD1.Sala(id),
    FOREIGN KEY (id_sala_destino) REFERENCES SBD1.Sala(id)
);


-- Criação das Funções do Jogo dentro do Schema SBD1

CREATE OR REPLACE FUNCTION SBD1.criar_personagem(
    p_nome_personagem VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_mensagem TEXT;
BEGIN
    INSERT INTO SBD1.Personagem(nome, id_sala_atual)
    VALUES (p_nome_personagem, 1) -- ID 1 = Recepção
    RETURNING 'Personagem "' || p_nome_personagem || '" criado com sucesso!' INTO v_mensagem;
    RETURN v_mensagem;
EXCEPTION
    WHEN unique_violation THEN
        RETURN 'Erro: Já existe um personagem com este nome.';
    WHEN OTHERS THEN
        RETURN 'Erro inesperado ao criar personagem.';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION SBD1.descrever_local_atual(
    p_id_personagem INT
) RETURNS TEXT AS $$
DECLARE
    v_descricao_sala TEXT;
    v_nome_sala_atual VARCHAR(100);
    v_saidas_disponiveis TEXT;
    v_id_sala_atual INT;
BEGIN
    SELECT P.id_sala_atual INTO v_id_sala_atual FROM SBD1.Personagem P WHERE P.id = p_id_personagem;

    IF v_id_sala_atual IS NULL THEN
        RETURN 'Erro: Personagem não encontrado ou sem localização definida.';
    END IF;

    SELECT S.nome, S.descricao INTO v_nome_sala_atual, v_descricao_sala FROM SBD1.Sala S WHERE S.id = v_id_sala_atual;

    SELECT string_agg(C.nome_saida, ', ') INTO v_saidas_disponiveis FROM SBD1.Conexao C WHERE C.id_sala_origem = v_id_sala_atual;

    IF v_saidas_disponiveis IS NULL THEN
        v_saidas_disponiveis := 'Nenhuma';
    END IF;

    RETURN 'Você está em: ' || v_nome_sala_atual || E'\n' || v_descricao_sala || E'\n\n' || 'Saídas disponíveis: ' || v_saidas_disponiveis;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION SBD1.mover_personagem(
    p_id_personagem INT,
    p_direcao_movimento VARCHAR(100)
) RETURNS TEXT AS $$
DECLARE
    v_id_sala_destino INT;
    v_id_sala_origem INT;
BEGIN
    SELECT P.id_sala_atual INTO v_id_sala_origem FROM SBD1.Personagem P WHERE P.id = p_id_personagem;

    SELECT C.id_sala_destino INTO v_id_sala_destino FROM SBD1.Conexao C WHERE C.id_sala_origem = v_id_sala_origem AND lower(C.nome_saida) = lower(p_direcao_movimento);

    IF v_id_sala_destino IS NOT NULL THEN
        UPDATE SBD1.Personagem SET id_sala_atual = v_id_sala_destino WHERE id = p_id_personagem;
        RETURN SBD1.descrever_local_atual(p_id_personagem);
    ELSE
        RETURN 'Você não pode ir por aí.';
    END IF;
END;
$$ LANGUAGE plpgsql;