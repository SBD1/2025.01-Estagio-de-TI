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
                WHERE n.andar_atual = (SELECT id_andar FROM Sala WHERE id_sala = %s);
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

l8h0ii-codex/adicionar-lógica-de-itens-e-npcs
def get_items_for_sale(item_type=None):
    """Lista itens disponíveis na loja, opcionalmente filtrando por tipo."""
    itens = []
    conn = get_connection()
    try:
        with conn.cursor() as cur:
       l8h0ii-codex/adicionar-lógica-de-itens-e-npcs
            if item_type:
                cur.execute(
                    """
                    SELECT ii.id_instancia, i.nome, i.descricao, i.preco_base, ii.quantidade
                    FROM InstanciaItem ii
                    JOIN Item i ON ii.id_item = i.id_item
                    WHERE ii.local_atual = 'Loja' AND i.tipo = %s
                    ORDER BY i.nome;
                    """,
                    (item_type,),
                )
            else:
                cur.execute(
                    """
                    SELECT ii.id_instancia, i.nome, i.descricao, i.preco_base, ii.quantidade
                    FROM InstanciaItem ii
                    JOIN Item i ON ii.id_item = i.id_item
                    WHERE ii.local_atual = 'Loja'
                    ORDER BY i.nome;
                    """
                )

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


def buy_item(personagem_id, instancia_id, quantidade):
    """Executa a compra de um item da loja."""
    return call_db_function("comprar_item", personagem_id, instancia_id, quantidade)
