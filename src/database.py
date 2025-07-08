import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import sys

# --- CONFIGURAÇÃO INICIAL ---
DB_HOST = "localhost"
DB_PORT = "6000"
DB_NAME = "jogo"
DB_USER = "jogador"
DB_PASS = "sbd1_password"

try:
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
except psycopg2.OperationalError as e:
    print(f"Erro CRÍTICO ao inicializar o pool de conexões: {e}")
    print("Verifique se o container Docker está rodando e as credenciais estão corretas.")
    db_pool = None
    sys.exit("Não foi possível conectar ao banco de dados. O programa será encerrado.")

@contextmanager
def db_session():
    """Fornece uma sessão de banco de dados transacional."""
    conn = None
    try:
        conn = db_pool.getconn()
        conn.autocommit = False
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            cur.close()
            db_pool.putconn(conn)

VALID_DB_FUNCTIONS = {
    'criar_personagem', 'comprar_item', 'usar_elevador', 'mover_personagem',
    'concluir_missao', 'usar_item', 'equipar_item', 'desequipar_item'
}

def call_db_function(function_name, *args):
    """Chama uma função PL/pgSQL do banco de dados de forma segura."""
    if function_name not in VALID_DB_FUNCTIONS:
        print(f"ALERTA DE SEGURANÇA: Tentativa de chamar função inválida '{function_name}'")
        return "Erro: Operação inválida."

    result = None
    try:
        with db_session() as cur:
            cur.execute(f"SELECT {function_name}({', '.join(['%s'] * len(args))});", args)
            if cur.description:
                result = cur.fetchone()[0]
    except Exception as e:
        print(f"Erro ao executar a função '{function_name}': {e}")
        return f"Erro inesperado ao executar a função: {e}"
    return result

def get_all_characters():
    """Busca todos os personagens jogáveis."""
    characters = []
    try:
        with db_session() as cur:
            cur.execute("""
                SELECT p.id_personagem, p.nome 
                FROM Personagem p
                JOIN Estagiario e ON p.id_personagem = e.id_personagem
                WHERE p.tipo = 'PC' 
                ORDER BY p.id_personagem;
            """)
            characters = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar personagens: {e}")
    return characters

def get_location_details(personagem_id):
    """Chama a função 'descrever_local_detalhado' e retorna os detalhes da sala."""
    details = None
    try:
        with db_session() as cur:
            cur.execute("SELECT * FROM descrever_local_detalhado(%s);", (personagem_id,))
            details = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar detalhes do local: {e}")
    return details

def get_player_room_info(personagem_id):
    """Retorna id, nome e descricao da sala atual do jogador."""
    info = None
    try:
        with db_session() as cur:
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
    return info

def get_npcs_in_room(sala_id):
    """Retorna lista de NPCs presentes na sala específica."""
    npcs = []
    try:
        with db_session() as cur:
            cur.execute(
                """
                SELECT p.id_personagem, p.nome, n.tipo
                FROM NPC n
                JOIN Personagem p ON n.id_personagem = p.id_personagem
                WHERE n.sala_atual = %s;
                """,
                (sala_id,),
            )
            npcs = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar NPCs na sala: {e}")
    return npcs

def get_items_for_sale(item_type=None):
    itens = []
    try:
        with db_session() as cur:
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
    return itens

def get_player_coins(personagem_id):
    coins = 0
    try:
        with db_session() as cur:
            cur.execute("SELECT coins FROM Estagiario WHERE id_personagem = %s;", (personagem_id,))
            res = cur.fetchone()
            if res:
                coins = res[0]
    except Exception as e:
        print(f"Erro ao buscar moedas do jogador: {e}")
    return coins

def get_player_stats(personagem_id):
    stats = None
    try:
        with db_session() as cur:
            cur.execute(
                """
                SELECT p.nome, e.nivel, e.xp, e.respeito, e.coins, e.ataque, e.defesa, e.vida, e.status
                FROM Estagiario e
                JOIN Personagem p ON e.id_personagem = p.id_personagem
                WHERE e.id_personagem = %s;
                """,
                (personagem_id,),
            )
            stats = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar status do jogador: {e}")
    return stats

def get_all_floors():
    andares = []
    try:
        with db_session() as cur:
            cur.execute("SELECT numero, nome FROM Andar ORDER BY numero;")
            andares = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar andares: {e}")
    return andares

def get_dialogue_for_npc(npc_id):
    dialogue = None
    try:
        with db_session() as cur:
            cur.execute("SELECT dialogo_padrao FROM npc WHERE id_personagem = %s;", (npc_id,))
            result = cur.fetchone()
            if result:
                dialogue = result[0]
    except Exception as e:
        print(f"Erro ao buscar diálogo do NPC: {e}")
    return dialogue

def get_available_missions_from_npc(player_id, npc_id):
    missions = []
    query = """
        SELECT m.id_missao, m.nome, m.dialogo_inicial
        FROM Missao m
        LEFT JOIN MissaoStatus ms ON m.id_missao = ms.id_missao AND ms.id_estagiario = %s
        WHERE m.npc_origem = %s AND (ms.status IS NULL OR ms.status = 'Disponível');
    """
    try:
        with db_session() as cur:
            cur.execute(query, (player_id, npc_id))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões do NPC: {e}")
    return missions

def accept_mission(player_id, mission_id):
    query = """
        INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
        VALUES (%s, %s, 'Em Andamento')
        ON CONFLICT (id_missao, id_estagiario)
        DO UPDATE SET status = 'Em Andamento';
    """
    try:
        with db_session() as cur:
            cur.execute(query, (mission_id, player_id))
        return True, "Missão aceita! Acompanhe em seu Painel de Tarefas."
    except Exception as e:
        print(f"Erro ao aceitar missão: {e}")
        return False, "Ocorreu um erro ao tentar aceitar a missão."

def get_player_missions(player_id):
    missions = []
    query = """
        SELECT m.nome, ms.status, m.descricao
        FROM Missao m
        JOIN MissaoStatus ms ON m.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s
        ORDER BY ms.status, m.nome;
    """
    try:
        with db_session() as cur:
            cur.execute(query, (player_id,))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões do jogador: {e}")
    return missions

def get_player_missions_status(player_id):
    missions_status = {}
    query = "SELECT id_missao, status FROM MissaoStatus WHERE id_estagiario = %s;"
    try:
        with db_session() as cur:
            cur.execute(query, (player_id,))
            results = cur.fetchall()
            for row in results:
                missions_status[row[0]] = row[1]
    except Exception as e:
        print(f"Erro ao buscar status das missões do jogador: {e}")
    return missions_status

def get_interactable_mission_in_room(player_id, sala_id):
    mission = None
    query = """
        SELECT m.id_missao, m.nome, m.tipo
        FROM Missao m
        JOIN MissaoStatus ms ON m.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s
          AND ms.status = 'Em Andamento'
          AND m.tipo = 'Manutenção'; 
    """
    try:
        with db_session() as cur:
            cur.execute(query, (player_id,))
            mission = cur.fetchone()
    except Exception as e:
        print(f"Erro ao verificar missão interativa na sala: {e}")
    return mission

def get_inimigos_na_sala(sala_id):
    """Retorna lista de inimigos presentes na sala específica."""
    inimigos = []
    query = """
        SELECT ii.id_instancia, i.nome, ii.vida, ii.dano, i.id_inimigo
        FROM InstanciaInimigo ii
        JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
        WHERE ii.sala_atual = %s;
    """
    try:
        with db_session() as cur:
            cur.execute(query, (sala_id,))
            inimigos = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar inimigos na sala: {e}")
    return inimigos

def get_missao_combate_ativa(player_id, mission_id):
    progresso = None
    query = """
        SELECT mc.quantidade_alvo, mc.quantidade_atual
        FROM MissaoCombate mc
        JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s AND ms.id_missao = %s AND ms.status = 'Em Andamento';
    """
    try:
        with db_session() as cur:
            cur.execute(query, (player_id, mission_id))
            progresso = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar progresso da missão de combate: {e}")
    return progresso

# ==================================================================
# == NOVA FUNÇÃO 1: get_active_combat_missions
# ==================================================================
def get_active_combat_missions(player_id):
    """Busca todas as missões de combate ativas para o jogador."""
    missions = []
    query = """
        SELECT mc.id_missao, mc.id_inimigo, mc.quantidade_alvo, mc.quantidade_atual
        FROM MissaoCombate mc
        JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
        WHERE ms.id_estagiario = %s AND ms.status = 'Em Andamento';
    """
    try:
        with db_session() as cur:
            cur.execute(query, (player_id,))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões de combate ativas: {e}")
    return missions

def atualizar_progresso_combate(mission_id):
    query = "UPDATE MissaoCombate SET quantidade_atual = quantidade_atual + 1 WHERE id_missao = %s;"
    try:
        with db_session() as cur:
            cur.execute(query, (mission_id,))
    except Exception as e:
        print(f"Erro ao atualizar progresso de combate: {e}")

# ==================================================================
# == NOVA FUNÇÃO 2: reset_player_location
# ==================================================================
def reset_player_location(player_id):
    """Move o jogador para a recepção e restaura parte da vida após a derrota."""
    try:
        with db_session() as cur:
            # IDs da sala e andar da recepção (Térreo, Sala Central)
            # Estes valores são baseados no seu arquivo DML.
            id_sala_recepcao = 7 
            id_andar_recepcao = 13

            cur.execute(
                """
                UPDATE Estagiario 
                SET vida = 50, sala_atual = %s, andar_atual = %s 
                WHERE id_personagem = %s;
                """,
                (id_sala_recepcao, id_andar_recepcao, player_id)
            )
    except Exception as e:
        print(f"Erro ao resetar a localização do jogador: {e}")


def get_player_inventory(personagem_id):
    inventory = []
    query = """
        SELECT inst.id_instancia, i.nome, ii.quantidade, i.descricao, i.tipo, 'Na Mochila' as status
        FROM Inventario inv
        JOIN ItemInventario ii ON inv.id_inventario = ii.id_inventario
        JOIN InstanciaItem inst ON ii.id_instancia = inst.id_instancia
        JOIN Item i ON inst.id_item = i.id_item
        WHERE inv.id_estagiario = %s
        UNION ALL
        SELECT inst.id_instancia, i.nome, 1 as quantidade, i.descricao, i.tipo, 'Equipado (' || ee.slot || ')' as status
        FROM EstagiarioEquipamento ee
        JOIN InstanciaItem inst ON ee.id_instancia = inst.id_instancia
        JOIN Item i ON inst.id_item = i.id_item
        WHERE ee.id_estagiario = %s
        ORDER BY tipo, nome;
    """
    try:
        with db_session() as cur:
            cur.execute(query, (personagem_id, personagem_id))
            inventory = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar inventário do jogador: {e}")
    return inventory

def buy_item(personagem_id, instancia_id, quantidade):
    return call_db_function("comprar_item", personagem_id, instancia_id, quantidade)

def use_elevator(personagem_id, andar_destino):
    return call_db_function("usar_elevador", personagem_id, andar_destino)

def complete_mission(player_id, mission_id):
    return call_db_function("concluir_missao", player_id, mission_id)

def use_item(personagem_id, instancia_id):
    return call_db_function("usar_item", personagem_id, instancia_id)

def equip_item(personagem_id, instancia_id):
    return call_db_function("equipar_item", personagem_id, instancia_id)

def unequip_item(personagem_id, instancia_id):
    return call_db_function("desequipar_item", personagem_id, instancia_id)