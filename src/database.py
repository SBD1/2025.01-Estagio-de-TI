import psycopg2

# Detalhes da conexão alinhados com o docker-compose.yml
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "jogo"
DB_USER = "jogador"
DB_PASS = "sbd1_password"

def get_connection():
    """Cria e retorna uma nova conexão com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        print("Verifique se o container Docker está rodando e as credenciais estão corretas.")
        return None

def call_db_function(function_name, *args):
    """Chama uma função no banco de dados (PL/pgSQL) e retorna o resultado."""
    result = None
    conn = get_connection()
    if not conn:
        return "[ERRO] Não foi possível conectar ao banco de dados."

    try:
        with conn.cursor() as cur:
            # CORREÇÃO: Adicionado o prefixo do schema SBD1.
            cur.execute(f"SELECT SBD1.{function_name}({', '.join(['%s'] * len(args))});", args)
            result = cur.fetchone()[0]
            conn.commit()
    except Exception as e:
        print(f"Erro ao executar a função '{function_name}': {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    return result

def get_all_characters():
    """Retorna uma lista de todos os personagens existentes."""
    characters = []
    conn = get_connection()
    if not conn:
        return characters

    try:
        with conn.cursor() as cur:
            # CORREÇÃO: Adicionado o prefixo do schema SBD1.
            cur.execute("SELECT id, nome FROM SBD1.Personagem ORDER BY id;")
            characters = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar personagens: {e}")
    finally:
        if conn:
            conn.close()
    return characters