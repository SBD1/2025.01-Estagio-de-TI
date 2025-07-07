import psycopg2

DB_HOST = "localhost"
DB_PORT = "6000"
DB_NAME = "jogo"
DB_USER = "jogador"
DB_PASS = "sbd1_password"

#Esse arquivo conecta e acessa o banco, pegando valores úteis para ser utilizados em funções com get


def get_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        print("Verifique se o container Docker está rodando e as credenciais estão corretas.")
        return None

def call_db_function(function_name, *args, tudo=False):
    result = None
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {function_name}({', '.join(['%s'] * len(args))});", args)
            if tudo == False:
                result = cur.fetchone()[0]
            elif tudo == True:
                result = cur.fetchall()
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
    
    #Chama a função 'descrever_local_detalhado' e retorna os detalhes
    #da sala de forma estruturada (nome, descricao, lista_de_saidas).
    
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

def get_dialogo_npc(id_npc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT dialogo FROM Dialogo WHERE id_npc = %s LIMIT 1;", (id_npc,))
        row = cur.fetchone()
    conn.close()
    return row[0] if row else "O NPC não tem nada a dizer."

def get_pcs_in_room(sala_id):
    conn = get_connection()
    result = []
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_pc, tipo FROM PC WHERE id_sala = %s
            """, (sala_id,))
            result = cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar PCs: {e}")
    finally:
        if conn:
            conn.close()
    return result

def get_inventario_itens(personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT i.nome, ii.quantidade
            FROM Inventario inv
            JOIN ItemInventario ii ON ii.id_inventario = inv.id_inventario
            JOIN InstanciaItem inst ON inst.id_instancia = ii.id_instancia
            JOIN Item i ON i.id_item = inst.id_item
            WHERE inv.id_estagiario = %s
        """, (personagem_id,))
        resultados = cur.fetchall()
    conn.close()
    return resultados
    
def get_itens_no_chao(sala_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT ii.id_instancia, i.nome
            FROM ItemNoChao nc
            JOIN InstanciaItem ii ON nc.id_instancia = ii.id_instancia
            JOIN Item i ON ii.id_item = i.id_item
            WHERE nc.id_sala = %s;
        """, (sala_id,))
        itens = cur.fetchall()
    conn.close()
    return itens

def pc_esta_inutilizavel(id_pc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT tipo FROM pc WHERE id_pc = %s;", (id_pc,))
        tipo = cur.fetchone()[0]
        if tipo == 'Bugado':
            return False  #PC bugado não tem limite de inimigos
        cur.execute("SELECT COUNT(*) FROM instanciainimigo WHERE id_pc = %s;", (id_pc,))
        return cur.fetchone()[0] >= 8
    conn.close()

def get_ataques_inimigo(id_inimigo):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.id_ataque, a.nome, a.dano, a.chance_acerto
            FROM Ataque a
            JOIN Inimigo_Ataque ia ON ia.id_ataque = a.id_ataque
            WHERE ia.id_inimigo = %s
        """, (id_inimigo,))
        ataques = cur.fetchall()
    conn.close()
    return ataques
