import random
from datetime import datetime, timedelta
from database import get_connection, pc_esta_inutilizavel


INIMIGOS_CONFIG = {
    1: {'nome': 'Bug', 'vida_min': 80, 'vida_max': 120, 'velocidade_min': 180, 'velocidade_max': 220},
    2: {'nome': 'Malware', 'vida_min': 400, 'vida_max': 600, 'velocidade_min': 80, 'velocidade_max': 120},
    3: {'nome': 'Hacker', 'vida_min': 800, 'vida_max': 1000, 'velocidade_min': 50, 'velocidade_max': 90}
}

def escolher_inimigo_aleatorio():
    return random.choice(list(INIMIGOS_CONFIG.keys()))

def contar_inimigos_no_pc(id_pc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM instanciainimigo WHERE id_pc = %s;", (id_pc,))
        return cur.fetchone()[0]
    conn.close()



def gerar_inimigo_no_pc(id_pc):
    id_inimigo = escolher_inimigo_aleatorio()
    config = INIMIGOS_CONFIG[id_inimigo]
    vida = random.randint(config['vida_min'], config['vida_max'])
    velocidade = random.randint(config['velocidade_min'], config['velocidade_max'])
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO instanciainimigo (id_inimigo, vida, velocidade, id_pc) VALUES (%s, %s, %s, %s);",
            (id_inimigo, vida, velocidade, id_pc)
        )
        conn.commit()
    conn.close()

def gerar_inimigo_automatico():
    """Gera inimigo automaticamente a cada 5 minutos em um PC aleatório"""
    conn = get_connection()
    with conn.cursor() as cur:
        # Busca todos os PCs que não são do tipo 'Bugado'
        cur.execute("SELECT id_pc FROM pc WHERE tipo != 'Bugado';")
        pcs_normais = [row[0] for row in cur.fetchall()]

        if not pcs_normais:
            conn.close()
            return

        # Escolhe um PC aleatório
        pc_aleatorio = random.choice(pcs_normais)

        # Verifica se o PC não está no limite
        if not pc_esta_inutilizavel(pc_aleatorio):
            gerar_inimigo_no_pc(pc_aleatorio)
            print(f"[SISTEMA] Um inimigo apareceu automaticamente no PC #{pc_aleatorio}!")

    conn.close()


def verificar_e_gerar_inimigos():

    conn = get_connection()
    with conn.cursor() as cur:
        # Verifica quando foi a última geração automática
        cur.execute("SELECT ultimo_acesso FROM pc WHERE id_pc = 1;")  # Usa PC 1 como referência de tempo
        resultado = cur.fetchone()
        ultimo_acesso = resultado[0] if resultado else None

        agora = datetime.now()

        # Se nunca gerou ou passaram 5 minutos
        if not ultimo_acesso or (agora - ultimo_acesso) >= timedelta(minutes=5):
            gerar_inimigo_automatico()
            # Atualiza o tempo de referência
            cur.execute("UPDATE pc SET ultimo_acesso = %s WHERE id_pc = 1;", (agora,))
            conn.commit()

    conn.close()

def listar_pcs_com_problemas():
    #Retorna lista de PCs que tem inimigos
    conn = get_connection()
    pcs_com_problemas = []
    with conn.cursor() as cur:
        # Busca todos os PCs que têm inimigos
        cur.execute("""
            SELECT DISTINCT id_pc
            FROM instanciainimigo
            ORDER BY id_pc;
        """)
        pcs_com_problemas = [row[0] for row in cur.fetchall()]

    conn.close()
    return pcs_com_problemas