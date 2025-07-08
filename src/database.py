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

def get_available_missions(player_id):
    """Retorna missões disponíveis para o jogador."""
    missions = []
    conn = get_connection()
    if not conn: return missions
    try:
        with conn.cursor() as cur:
            query = """
                SELECT m.id_missao, m.nome, m.descricao, m.tipo, m.xp_recompensa, m.moedas_recompensa,
                       COALESCE(ms.status, 'Disponível') as status
                FROM Missao m
                LEFT JOIN MissaoStatus ms ON m.id_missao = ms.id_missao AND ms.id_estagiario = %s
                LEFT JOIN MissaoConcluida mc ON m.id_missao = mc.id_missao AND mc.id_estagiario = %s
                WHERE mc.id_missao IS NULL
                ORDER BY m.id_missao;
            """
            cur.execute(query, (player_id, player_id))
            missions = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar missões: {e}")
    finally:
        if conn: conn.close()
    return missions

def accept_mission(player_id, mission_id):
    """Aceita uma missão para o jogador."""
    conn = get_connection()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
                VALUES (%s, %s, 'Em Andamento')
                ON CONFLICT (id_missao, id_estagiario) 
                DO UPDATE SET status = 'Em Andamento'
            """, (mission_id, player_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao aceitar missão: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_mission_details(mission_id):
    """Retorna detalhes específicos de uma missão."""
    details = None
    conn = get_connection()
    if not conn: return details
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT m.id_missao, m.nome, m.descricao, m.dialogo_inicial, m.tipo, 
                       m.xp_recompensa, m.moedas_recompensa, m.npc_origem
                FROM Missao m WHERE m.id_missao = %s
            """, (mission_id,))
            details = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar detalhes da missão: {e}")
    finally:
        if conn: conn.close()
    return details

def complete_mission(player_id, mission_id):
    """Completa uma missão e dá recompensas."""
    conn = get_connection()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            # Busca dados da missão
            cur.execute("SELECT xp_recompensa, moedas_recompensa FROM Missao WHERE id_missao = %s", (mission_id,))
            mission_data = cur.fetchone()
            
            if not mission_data:
                return False
                
            xp_reward, coins_reward = mission_data
            
            # Marca como concluída
            cur.execute("""
                INSERT INTO MissaoConcluida (id_missao, id_estagiario, xp_ganho, moedas_ganhas)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_missao, id_estagiario) DO NOTHING
            """, (mission_id, player_id, xp_reward, coins_reward))
            
            # Atualiza status
            cur.execute("""
                UPDATE MissaoStatus 
                SET status = 'Concluída' 
                WHERE id_missao = %s AND id_estagiario = %s
            """, (mission_id, player_id))
            
            # Dá recompensas
            cur.execute("""
                UPDATE Estagiario 
                SET xp = xp + %s, coins = coins + %s
                WHERE id_personagem = %s
            """, (xp_reward, coins_reward, player_id))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao completar missão: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_player_inventory(player_id):
    """Retorna o inventário do jogador."""
    items = []
    conn = get_connection()
    if not conn: return items
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT i.id_item, i.nome, i.descricao, ii.quantidade 
                FROM ItemInventario ii
                JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
                JOIN InstanciaItem ins ON ii.id_instancia = ins.id_instancia
                JOIN Item i ON ins.id_item = i.id_item
                WHERE inv.id_estagiario = %s
            """, (player_id,))
            items = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar inventário: {e}")
    finally:
        if conn: conn.close()
    return items

def get_npcs_in_location(player_id):
    """Retorna NPCs na localização atual do jogador."""
    npcs = []
    conn = get_connection()
    if not conn: return npcs
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT n.id_personagem, p.nome, n.tipo, n.dialogo_padrao
                FROM NPC n
                JOIN Personagem p ON n.id_personagem = p.id_personagem
                JOIN Estagiario e ON n.andar_atual = e.andar_atual
                WHERE e.id_personagem = %s
            """, (player_id,))
            npcs = cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar NPCs: {e}")
    finally:
        if conn: conn.close()
    return npcs

def get_enemies_in_location(player_id):
    """Retorna inimigos na mesma localização do jogador (ou todos os inimigos vivos)."""
    conn = get_connection()
    if not conn: return []
    try:
        with conn.cursor() as cur:
            # Como InstanciaInimigo não tem campo de sala, retorna todos os inimigos vivos
            cur.execute("""
                SELECT ii.id_instancia, i.nome, ii.vida, ii.dano, i.ataque
                FROM InstanciaInimigo ii
                JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
                WHERE ii.vida > 0
                ORDER BY i.nome
            """)
            return cur.fetchall()
    except Exception as e:
        print(f"Erro ao buscar inimigos: {e}")
        return []
    finally:
        if conn: conn.close()

def attack_enemy(player_id, enemy_instance_id):
    """Ataca um inimigo."""
    conn = get_connection()
    if not conn: return False, "Erro de conexão"
    try:
        with conn.cursor() as cur:
            # Verifica se inimigo existe e está vivo
            cur.execute("""
                SELECT ii.vida, ii.dano, i.id_inimigo, i.nome
                FROM InstanciaInimigo ii
                JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
                WHERE ii.id_instancia = %s AND ii.vida > 0
            """, (enemy_instance_id,))
            enemy_data = cur.fetchone()
            
            if not enemy_data:
                return False, "Inimigo não encontrado ou já foi derrotado"
                
            enemy_hp, enemy_damage, enemy_id, enemy_name = enemy_data
            
            # Calcula dano do jogador (base 50 + random)
            import random
            player_damage = random.randint(40, 60)
            
            # Aplica dano ao inimigo
            new_enemy_hp = max(0, enemy_hp - player_damage)
            cur.execute("UPDATE InstanciaInimigo SET vida = %s WHERE id_instancia = %s", (new_enemy_hp, enemy_instance_id))
            
            result_msg = f"⚔️ Você causou {player_damage} de dano!"
            
            if new_enemy_hp <= 0:
                result_msg += f" 💀 {enemy_name} derrotado!"
                # Dá XP pela vitória
                cur.execute("UPDATE Estagiario SET xp = xp + 25 WHERE id_personagem = %s", (player_id,))
                
                # Atualiza progresso das missões de combate
                cur.execute("""
                    SELECT mc.id_missao, mc.quantidade_atual, mc.quantidade_alvo
                    FROM MissaoCombate mc
                    JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
                    WHERE ms.id_estagiario = %s 
                    AND ms.status = 'Em Andamento'
                    AND mc.id_inimigo = %s
                """, (player_id, enemy_id))
                
                combat_missions = cur.fetchall()
                
                for mission_id, current, target in combat_missions:
                    if current < target:
                        new_progress = current + 1
                        cur.execute("""
                            UPDATE MissaoCombate 
                            SET quantidade_atual = %s
                            WHERE id_missao = %s
                        """, (new_progress, mission_id))
                        result_msg += f" [Missão: {new_progress}/{target}]"
                
            else:
                result_msg += f" 🩸 {enemy_name} ainda tem {new_enemy_hp} HP."
                # Inimigo contra-ataca
                cur.execute("UPDATE Estagiario SET coins = coins - 3 WHERE id_personagem = %s AND coins > 0", (player_id,))
                result_msg += f" 🗡️ Contra-ataque! (-3 coins)"
            
            conn.commit()
            
            # Verifica se alguma missão foi completada
            completed = check_and_complete_missions(player_id)
            if completed:
                result_msg += "\n" + "\n".join(completed)
            
            return True, result_msg
    except Exception as e:
        print(f"Erro no combate: {e}")
        if conn: conn.rollback()
        return False, f"Erro no combate: {e}"
    finally:
        if conn: conn.close()

def check_mission_completion(player_id, mission_id):
    """Verifica se uma missão pode ser completada."""
    conn = get_connection()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            # Busca tipo da missão
            cur.execute("SELECT tipo FROM Missao WHERE id_missao = %s", (mission_id,))
            mission_type = cur.fetchone()
            
            if not mission_type:
                return False
                
            mission_type = mission_type[0]
            
            if mission_type == 'Combate':
                # Verifica se matou inimigos suficientes
                cur.execute("""
                    SELECT mc.quantidade_alvo, mc.quantidade_atual
                    FROM MissaoCombate mc
                    WHERE mc.id_missao = %s
                """, (mission_id,))
                combat_data = cur.fetchone()
                if combat_data:
                    target, current = combat_data
                    return current >= target
                    
            elif mission_type == 'Conversa':
                # Para missões de conversa, considera completa se foi aceita
                # (simplificação para o teste)
                return True
                
            elif mission_type == 'Entrega':
                # Verifica se tem item necessário no inventário
                cur.execute("""
                    SELECT me.id_item, me.quantidade
                    FROM MissaoEntrega me
                    WHERE me.id_missao = %s
                """, (mission_id,))
                delivery_data = cur.fetchone()
                if delivery_data:
                    item_id, required_qty = delivery_data
                    # Verifica se tem o item no inventário
                    cur.execute("""
                        SELECT COALESCE(SUM(ii.quantidade), 0)
                        FROM ItemInventario ii
                        JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
                        JOIN InstanciaItem ins ON ii.id_instancia = ins.id_instancia
                        WHERE inv.id_estagiario = %s AND ins.id_item = %s
                    """, (player_id, item_id))
                    current_qty = cur.fetchone()[0]
                    return current_qty >= required_qty
                    
            elif mission_type == 'Manutenção':
                # Para missões de manutenção, considera completa se foi aceita
                # (simplificação para o teste)
                return True
                    
            return False
    except Exception as e:
        print(f"Erro ao verificar missão: {e}")
        return False
    finally:
        if conn: conn.close()

def update_combat_mission_progress(player_id, enemy_id):
    """Atualiza progresso de missões de combate."""
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            # Busca missões de combate em andamento para este inimigo
            cur.execute("""
                SELECT mc.id_missao, mc.quantidade_atual, mc.quantidade_alvo
                FROM MissaoCombate mc
                JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
                WHERE ms.id_estagiario = %s 
                AND ms.status = 'Em Andamento'
                AND mc.id_inimigo = %s
            """, (player_id, enemy_id))
            
            combat_missions = cur.fetchall()
            
            for mission_id, current, target in combat_missions:
                if current < target:
                    cur.execute("""
                        UPDATE MissaoCombate 
                        SET quantidade_atual = quantidade_atual + 1
                        WHERE id_missao = %s
                    """, (mission_id,))
                    print(f"🎯 Progresso da missão atualizado: {current + 1}/{target}")
            
            conn.commit()
    except Exception as e:
        print(f"Erro ao atualizar progresso: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

def get_player_status(player_id):
    """Retorna o status completo do jogador."""
    status = None
    conn = get_connection()
    if not conn: return status
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.nome, e.nivel, e.xp, e.coins, e.status, a.nome, s.nome
                FROM Estagiario e
                JOIN Personagem p ON e.id_personagem = p.id_personagem
                JOIN Andar a ON e.andar_atual = a.id_andar
                JOIN Sala s ON e.sala_atual = s.id_sala
                WHERE e.id_personagem = %s
            """, (player_id,))
            status = cur.fetchone()
    except Exception as e:
        print(f"Erro ao buscar status: {e}")
    finally:
        if conn: conn.close()
    return status

def get_player_achievements(player_id):
    """Retorna as conquistas do jogador (funcionalidade simplificada)."""
    # Por enquanto, retorna lista vazia pois não temos sistema de conquistas implementado
    return []

def check_and_grant_achievements(player_id):
    """Verifica conquistas (funcionalidade simplificada)."""
    # Por enquanto, retorna mensagem vazia
    return "Nenhuma conquista nova."

def complete_delivery_mission(player_id, mission_id):
    """Completa uma missão de entrega (versão simplificada)."""
    conn = get_connection()
    if not conn: return False, "Erro de conexão"
    try:
        with conn.cursor() as cur:
            # Busca dados da missão de entrega
            cur.execute("""
                SELECT me.id_item, me.quantidade
                FROM MissaoEntrega me
                WHERE me.id_missao = %s
            """, (mission_id,))
            delivery_data = cur.fetchone()
            
            if not delivery_data:
                return False, "Missão de entrega não encontrada!"
                
            item_id, required_qty = delivery_data
            
            # Verifica se tem o item no inventário
            cur.execute("""
                SELECT COALESCE(SUM(ii.quantidade), 0)
                FROM ItemInventario ii
                JOIN Inventario inv ON ii.id_inventario = inv.id_inventario
                JOIN InstanciaItem ins ON ii.id_instancia = ins.id_instancia
                WHERE inv.id_estagiario = %s AND ins.id_item = %s
            """, (player_id, item_id))
            current_qty = cur.fetchone()[0]
            
            if current_qty < required_qty:
                return False, 'Você não tem os itens necessários para completar esta missão!'
            
            # Por simplicidade, não remove o item do inventário no teste
            # Em uma implementação completa, removeria os itens aqui
            
            return True, 'Missão de entrega completada! Itens entregues.'
            
    except Exception as e:
        print(f"Erro na entrega: {e}")
        if conn: conn.rollback()
        return False, f"Erro na entrega: {e}"
    finally:
        if conn: conn.close()

def get_mission_progress(player_id, mission_id):
    """Retorna o progresso de uma missão específica."""
    progress = None
    conn = get_connection()
    if not conn: return progress
    try:
        with conn.cursor() as cur:
            # Busca tipo da missão
            cur.execute("SELECT tipo FROM Missao WHERE id_missao = %s", (mission_id,))
            mission_type = cur.fetchone()
            
            if not mission_type:
                return None
                
            mission_type = mission_type[0]
            
            if mission_type == 'Combate':
                cur.execute("""
                    SELECT mc.quantidade_atual, mc.quantidade_alvo, i.nome
                    FROM MissaoCombate mc
                    JOIN Inimigo i ON mc.id_inimigo = i.id_inimigo
                    WHERE mc.id_missao = %s
                """, (mission_id,))
                progress = cur.fetchone()
                if progress:
                    current, target, enemy_name = progress
                    return f"Progresso: {current}/{target} {enemy_name}s eliminados"
            
            elif mission_type == 'Entrega':
                cur.execute("""
                    SELECT me.quantidade, i.nome, p.nome
                    FROM MissaoEntrega me
                    JOIN Item i ON me.id_item = i.id_item
                    JOIN NPC n ON me.id_npc_destino = n.id_personagem
                    JOIN Personagem p ON n.id_personagem = p.id_personagem
                    WHERE me.id_missao = %s
                """, (mission_id,))
                progress = cur.fetchone()
                if progress:
                    qty, item_name, npc_name = progress
                    return f"Entregar: {qty}x {item_name} para {npc_name}"
            
            elif mission_type == 'Conversa':
                cur.execute("""
                    SELECT p.nome
                    FROM MissaoConversa mc
                    JOIN NPC n ON mc.id_npc_alvo = n.id_personagem
                    JOIN Personagem p ON n.id_personagem = p.id_personagem
                    WHERE mc.id_missao = %s
                """, (mission_id,))
                progress = cur.fetchone()
                if progress:
                    npc_name = progress[0]
                    return f"Conversar com: {npc_name}"
            
            else:
                return "Missão de manutenção - Complete as tarefas necessárias"
                
    except Exception as e:
        print(f"Erro ao buscar progresso: {e}")
    finally:
        if conn: conn.close()
    return progress

def update_player_name(player_id, new_name):
    """Atualiza o nome do personagem."""
    conn = get_connection()
    if not conn: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Personagem 
                SET nome = %s 
                WHERE id_personagem = %s
            """, (new_name, player_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao atualizar nome: {e}")
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def check_and_complete_missions(player_id):
    """Verifica e completa automaticamente missões que atingiram o objetivo."""
    conn = get_connection()
    if not conn: return []
    completed_missions = []
    try:
        with conn.cursor() as cur:
            # Busca missões de combate prontas para completar
            cur.execute("""
                SELECT mc.id_missao, m.nome, m.xp_recompensa, m.moedas_recompensa
                FROM MissaoCombate mc
                JOIN Missao m ON mc.id_missao = m.id_missao
                JOIN MissaoStatus ms ON mc.id_missao = ms.id_missao
                WHERE ms.id_estagiario = %s 
                AND ms.status = 'Em Andamento'
                AND mc.quantidade_atual >= mc.quantidade_alvo
            """, (player_id,))
            
            combat_missions = cur.fetchall()
            
            for mission_id, nome, xp_reward, coin_reward in combat_missions:
                # Marca como concluída
                cur.execute("""
                    UPDATE MissaoStatus 
                    SET status = 'Concluída' 
                    WHERE id_missao = %s AND id_estagiario = %s
                """, (mission_id, player_id))
                
                # Adiciona às missões concluídas
                cur.execute("""
                    INSERT INTO MissaoConcluida (id_estagiario, id_missao, data_conclusao)
                    VALUES (%s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT DO NOTHING
                """, (player_id, mission_id))
                
                # Dá recompensas
                cur.execute("""
                    UPDATE Estagiario 
                    SET xp = xp + %s, coins = coins + %s 
                    WHERE id_personagem = %s
                """, (xp_reward, coin_reward, player_id))
                
                completed_missions.append(f"🎉 {nome} CONCLUÍDA! +{xp_reward} XP, +{coin_reward} moedas")
            
            conn.commit()
            return completed_missions
    except Exception as e:
        print(f"Erro ao verificar conclusões: {e}")
        if conn: conn.rollback()
        return []
    finally:
        if conn: conn.close()

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

