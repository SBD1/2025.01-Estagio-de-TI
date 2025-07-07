import psycopg2

DB_HOST = "localhost"
DB_PORT = "6000"
DB_NAME = "jogo"
DB_USER = "jogador"
DB_PASS = "sbd1_password"

def get_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        print("Verifique se o container Docker está rodando e as credenciais estão corretas.")
        return None

def call_db_function(function_name, *args):
    result = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {function_name}({', '.join(['%s'] * len(args))});", args)
            if cur.description:
                result = cur.fetchone()[0]
            conn.commit()
    except Exception as e:
        print(f"Erro ao executar a função '{function_name}': {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()
    return result

def get_all_characters():
    characters = []
    conn = get_connection()
    if not conn: return characters
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_personagem, nome FROM Estagiario ORDER BY id_personagem;")
            characters = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar personagens: {e}")
    finally:
        if conn: conn.close()
    return characters

def get_location_details(personagem_id):
    """
    Chama a função 'descrever_local_detalhado' e retorna os detalhes
    da sala de forma estruturada (nome, descricao, lista_de_saidas).
    """
    details = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM descrever_local_detalhado(%s);", (personagem_id,))
            details = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar detalhes do local: {e}")
    finally:
        if conn:
            conn.close()
    return details


def get_player_room_info(personagem_id):
    """Retorna id, nome e descricao da sala atual do jogador."""
    info = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.id_sala, s.nome, s.descricao
                FROM Sala s
                JOIN Estagiario e ON s.id_sala = e.sala_atual
                WHERE e.id_personagem = %s;
                """,
                (personagem_id,),
            )
            info = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar sala atual: {e}")
    finally:
        if conn:
            conn.close()
    return info


def get_npcs_in_room(sala_id):
    """Retorna lista de NPCs presentes na sala."""
    npcs = []
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.id_personagem, p.nome, n.tipo
                FROM NPC n
                JOIN Personagem p ON n.id_personagem = p.id_personagem
                JOIN Sala s ON n.andar_atual = s.id_andar
                WHERE s.id_sala = %s;
                """,
                (sala_id,),
            )
            npcs = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar NPCs: {e}")
    finally:
        if conn:
            conn.close()
    return npcs

def get_items_for_sale(item_type=None):
    """Lista itens disponíveis na loja, opcionalmente filtrando por tipo."""
    itens = []
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            base_query = """
                SELECT ii.id_instancia, i.nome, i.descricao, i.preco_base, ii.quantidade,
                       COALESCE(e.bonus_ataque, 0) AS bonus_ataque,
                       COALESCE(e.bonus_defesa, 0) AS bonus_defesa,
                       COALESCE(c.recuperacao_vida, 0) AS recuperacao_vida
                FROM InstanciaItem ii
                JOIN Item i ON ii.id_item = i.id_item
                LEFT JOIN Equipamento e ON i.id_item = e.id_item
                LEFT JOIN Consumivel c ON i.id_item = c.id_item
                WHERE ii.local_atual = 'Loja'
            """
            params = []
            if item_type:
                base_query += " AND i.tipo = %s"
                params.append(item_type)

            base_query += " ORDER BY i.nome;"

            cur.execute(base_query, params)
            itens = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar itens da loja: {e}")
    finally:
        if conn:
            conn.close()
    return itens

def get_player_coins(personagem_id):
    """Retorna a quantidade atual de moedas do jogador."""
    coins = 0
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT coins FROM Estagiario WHERE id_personagem = %s;",
                (personagem_id,),
            )
            res = cur.fetchone()
            if res:
                coins = res[0]
    except Exception as e:
        print(f"Erro ao buscar moedas do jogador: {e}")
    finally:
        if conn:
            conn.close()
    return coins


def get_player_stats(personagem_id):
    """Retorna status completo do jogador."""
    stats = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT nome, nivel, xp, respeito, coins, ataque, defesa, vida, status
                FROM Estagiario
                WHERE id_personagem = %s;
                """,
                (personagem_id,),
            )
            stats = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar status do jogador: {e}")
    finally:
        if conn:
            conn.close()
    return stats


def buy_item(personagem_id, instancia_id, quantidade):
    """Executa a compra de um item da loja."""
    return call_db_function("comprar_item", personagem_id, instancia_id, quantidade)


def use_elevator(personagem_id, andar_destino):
    """Chama a função do banco de dados para usar o elevador."""
    return call_db_function("usar_elevador", personagem_id, andar_destino)

def get_all_floors():
    """Retorna uma lista de todos os andares (numero, nome)."""
    andares = []
    conn = get_connection()
    if not conn: return andares
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT numero, nome FROM Andar ORDER BY numero;")
            andares = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar andares: {e}")
    finally:
        if conn: conn.close()
    return andares

# =================================================================
# == FUNÇÕES PARA O SISTEMA DE MISSÕES E INTERAÇÕES ==
# =================================================================

def get_dialogue_for_npc(npc_id):
    """Busca o diálogo padrão de um NPC."""
    dialogue = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT dialogo_padrao FROM npc WHERE id_personagem = %s;", (npc_id,))
            result = cur.fetchone()
            if result:
                dialogue = result[0]
    except Exception as e:
        print(f"Erro ao buscar diálogo do NPC: {e}")
    finally:
        if conn:
            conn.close()
    return dialogue

def get_available_missions_from_npc(player_id, npc_id):
    """Verifica se um NPC tem missões disponíveis para o jogador."""
    missions = []
    conn = get_connection()
    query = """
        SELECT m.id_missao, m.nome, m.dialogo_inicial
        FROM Missao m
        LEFT JOIN MissaoStatus ms ON m.id_missao = ms.id_missao AND ms.id_estagiario = %s
        WHERE m.npc_origem = %s AND (ms.status IS NULL OR ms.status = 'Disponível');
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (player_id, npc_id))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões do NPC: {e}")
    finally:
        if conn:
            conn.close()
    return missions

def accept_mission(player_id, mission_id):
    """Registra que um jogador aceitou uma missão, mudando seu status para 'Em Andamento'."""
    conn = get_connection()
    if not conn: return False, "Falha na conexão com o banco."
    
    query = """
        INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
        VALUES (%s, %s, 'Em Andamento')
        ON CONFLICT (id_missao, id_estagiario)
        DO UPDATE SET status = 'Em Andamento';
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (mission_id, player_id))
            conn.commit()
            return True, "Missão aceita! Acompanhe em seu Painel de Tarefas."
    except Exception as e:
        if conn: conn.rollback()
        print(f"Erro ao aceitar missão: {e}")
        return False, "Ocorreu um erro ao tentar aceitar a missão."
    finally:
        if conn: conn.close()

def get_player_missions(player_id):
    """Busca todas as missões (em andamento ou concluídas) de um jogador."""
    missions = []
    conn = get_connection()
    query = """
        SELECT m.nome, ms.status, m.descricao
        FROM Missao m
        JOIN MissaoStatus ms ON m.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s
        ORDER BY ms.status, m.nome;
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (player_id,))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões do jogador: {e}")
    finally:
        if conn: conn.close()
    return missions

def get_player_missions_status(player_id):
    """Retorna um dicionário simples com o status de todas as missões de um jogador."""
    missions_status = {}
    conn = get_connection()
    query = "SELECT id_missao, status FROM MissaoStatus WHERE id_estagiario = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(query, (player_id,))
            results = cur.fetchall()
            for row in results:
                missions_status[row[0]] = row[1]
    except Exception as e:
        print(f"Erro ao buscar status das missões do jogador: {e}")
    finally:
        if conn:
            conn.close()
    return missions_status

def get_interactable_mission_in_room(player_id, sala_id):
    """Verifica se há uma missão de MANUTENÇÃO ativa na sala atual do jogador."""
    mission = None
    conn = get_connection()
    if sala_id != 2: # A missão 'Check-up no Servidor' ocorre na sala com id=2 ('Data Center')
        return None
        
    query = """
        SELECT m.id_missao, m.nome, m.tipo
        FROM Missao m
        JOIN MissaoStatus ms ON m.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s
          AND ms.status = 'Em Andamento'
          AND m.tipo = 'Manutenção'
          AND m.nome = 'Check-up no Servidor';
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (player_id,))
            mission = cur.fetchone()
    except Exception as e:
        print(f"Erro ao verificar missão interativa na sala: {e}")
    finally:
        if conn: conn.close()
    return mission

# ---- FUNÇÕES DE COMBATE ----
def get_inimigos_na_sala(sala_id):
    """Busca instâncias de inimigos que podem aparecer na sala atual do jogador."""
    inimigos = []
    conn = get_connection()
    query = """
        SELECT ii.id_instancia, i.nome, ii.vida, ii.dano, m.id_missao
        FROM InstanciaInimigo ii
        JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
        JOIN MissaoCombate mc ON i.id_inimigo = mc.id_inimigo
        JOIN Missao m ON mc.id_missao = m.id_missao
        JOIN Estagiario e ON m.npc_origem = e.id_personagem -- Lógica simplificada de localização
        WHERE e.sala_atual = %s AND m.id_missao IN (
            SELECT ms.id_missao FROM MissaoStatus ms
            WHERE ms.id_estagiario = e.id_personagem AND ms.status = 'Em Andamento'
        );
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (sala_id,))
            inimigos = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar inimigos na sala: {e}")
    finally:
        if conn: conn.close()
    return inimigos

def get_missao_combate_ativa(player_id, mission_id):
    """Busca o progresso de uma missão de combate (alvo vs atual)."""
    progresso = None
    conn = get_connection()
    query = """
        SELECT mc.quantidade_alvo, mc.quantidade_atual
        FROM MissaoCombate mc
        JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s AND ms.id_missao = %s AND ms.status = 'Em Andamento';
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (player_id, mission_id))
            progresso = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar progresso da missão de combate: {e}")
    finally:
        if conn: conn.close()
    return progresso

def atualizar_progresso_combate(mission_id):
    """Incrementa o contador de inimigos derrotados para uma missão."""
    conn = get_connection()
    query = "UPDATE MissaoCombate SET quantidade_atual = quantidade_atual + 1 WHERE id_missao = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(query, (mission_id,))
            conn.commit()
    except Exception as e:
        if conn: conn.rollback()
        print(f"Erro ao atualizar progresso de combate: {e}")
    finally:
        if conn: conn.close()

# ---- FUNÇÃO DE CONCLUSÃO DE MISSÃO ----
def complete_mission(player_id, mission_id):
    """Chama a função do banco de dados para concluir a missão e obter as recompensas."""
    return call_db_function("concluir_missao", player_id, mission_id)