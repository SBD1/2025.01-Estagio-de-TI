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

def get_sala_id(personagem_id):
    sala_id = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT sala_atual FROM Estagiario WHERE id_personagem = %s;", (personagem_id,))
            row = cur.fetchone()
            if row:
                sala_id = row[0]
    except Exception as e:
        print(f"Erro ao buscar sala do personagem: {e}")
    finally:
        if conn:
            conn.close()
    return sala_id
    
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

def get_npcs_in_room(sala_id):
    conn = get_connection()
    result = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT n.id_personagem, p.nome, n.tipo
                FROM NPC n
                JOIN Personagem p ON n.id_personagem = p.id_personagem
                WHERE p.id_sala = %s
            """, (sala_id,))
            result = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar NPCs: {e}")
    finally:
        if conn:
            conn.close()
    return resulty

def get_pcs_in_room(sala_id):
    conn = get_connection()
    result = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_pc FROM PC WHERE id_sala = %s
            """, (sala_id,))
            result = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar PCs: {e}")
    finally:
        if conn:
            conn.close()
    return result