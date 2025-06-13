import psycopg2
import os

# Detalhes da conexão. Use variáveis de ambiente para segurança em produção.
# Para este projeto, vamos colocar diretamente.
# O 'host' é 'localhost' porque o docker-compose.yml mapeia a porta 5432 do container para a 5432 do seu computador.
DB_HOST = "localhost"
DB_PORT = "5432" # Porta mapeada no docker-compose
DB_NAME = "sbd1"
DB_USER = "sbd1"
DB_PASS = "22312"

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
    """
    Chama uma função no banco de dados (PL/pgSQL) e retorna o resultado.
    """
    result = None
    conn = get_connection()
    if not conn:
        return "[ERRO] Não foi possível conectar ao banco de dados."

    try:
        with conn.cursor() as cur:
            # O formato da chamada é 'SELECT schema.function_name(%s, %s, ...)'
            # psycopg2 vai substituir os %s pelos argumentos em 'args' de forma segura.
            cur.execute(f"SELECT SBD1.{function_name}({', '.join(['%s'] * len(args))});", args)
            # Pega o primeiro (e único) resultado da chamada da função.
            result = cur.fetchone()[0]
            conn.commit()
    except Exception as e:
        print(f"Erro ao executar a função '{function_name}': {e}")
        if conn:
            conn.rollback() # Desfaz a transação em caso de erro
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
            cur.execute("SELECT id, nome FROM SBD1.Personagem ORDER BY id;")
            characters = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar personagens: {e}")
    finally:
        if conn:
            conn.close()
    return characters