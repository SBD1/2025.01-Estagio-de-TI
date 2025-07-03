import psycopg2
import sys

class DatabaseController:
    """
    Controlador do banco de dados para o jogo 'A Saga do Estagiário'.
    Gerencia todas as conexões e transações com o PostgreSQL.
    """
    def __init__(self, dbname="saga_estagiario_db", user="postgres", password="postgres", host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self._create_database()

    def _create_database(self):
        """Cria o banco de dados se ele não existir."""
        try:
            conn = psycopg2.connect(dbname="postgres", user=self.user, password=self.password, host=self.host, port=self.port)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.dbname}'")
            if not cursor.fetchone():
                cursor.execute(f"CREATE DATABASE {self.dbname}")
                print(f"Banco de dados '{self.dbname}' criado com sucesso.")
            else:
                print(f"Banco de dados '{self.dbname}' já existe.")
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            print(f"Erro de conexão com o PostgreSQL: {e}", file=sys.stderr)
            print("Verifique se o serviço do PostgreSQL está rodando e as credenciais estão corretas.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Erro inesperado ao verificar/criar banco de dados: {e}", file=sys.stderr)
            sys.exit(1)


    def connect(self):
        """Estabelece a conexão com o banco de dados do jogo."""
        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port
                )
            except psycopg2.OperationalError as e:
                print(f"Não foi possível conectar ao banco de dados '{self.dbname}': {e}", file=sys.stderr)
                sys.exit(1)

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def execute_sql_script(self, script_path):
        """Executa um script SQL a partir de um arquivo."""
        try:
            with open(script_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                cursor = self.conn.cursor()
                cursor.execute(sql_script)
                self.conn.commit()
                cursor.close()
                print(f"Script '{script_path}' executado com sucesso.")
        except FileNotFoundError:
            print(f"Erro: Arquivo de script não encontrado em '{script_path}'", file=sys.stderr)
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao executar o script SQL '{script_path}': {e}", file=sys.stderr)

    def add_estagiario(self, nome):
        """Adiciona um novo personagem estagiário ao banco de dados."""
        try:
            cursor = self.conn.cursor()
            # Insere na tabela Personagem e obtém o ID
            cursor.execute(
                "INSERT INTO Personagem (nome, tipo, descricao) VALUES (%s, 'PC', 'Jovem sonhador em busca da efetivação.') RETURNING id_personagem",
                (nome,)
            )
            id_personagem = cursor.fetchone()[0]

            # Insere na tabela Estagiario com valores iniciais
            # Sala 7 = Sala Central do Térreo, Andar 13 = Térreo (número 0)
            cursor.execute(
                "INSERT INTO Estagiario (id_personagem, xp, nivel, coins, status, andar_atual, sala_atual) VALUES (%s, 0, 1, 10, 'Normal', 13, 7)",
                (id_personagem,)
            )
            
            # Cria o inventário para o novo estagiário
            cursor.execute("INSERT INTO Inventario (id_estagiario) VALUES (%s)", (id_personagem,))

            self.conn.commit()
            print(f"Estagiário '{nome}' criado com sucesso!")
            cursor.close()
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao adicionar estagiário: {e}", file=sys.stderr)

    def get_registered_players(self):
        """Retorna uma lista de tuplas (id, nome) de todos os estagiários."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_personagem, nome FROM Personagem WHERE tipo = 'PC' ORDER BY id_personagem")
        jogadores = cursor.fetchall()
        cursor.close()
        return jogadores

    def get_player_status(self, player_id):
        """Busca o status completo do jogador."""
        cursor = self.conn.cursor()
        query = """
            SELECT p.nome, e.nivel, e.xp, e.coins, e.status, s.nome as sala_nome, a.nome as andar_nome
            FROM Estagiario e
            JOIN Personagem p ON e.id_personagem = p.id_personagem
            JOIN Sala s ON e.sala_atual = s.id_sala
            JOIN Andar a ON s.id_andar = a.id_andar
            WHERE e.id_personagem = %s;
        """
        cursor.execute(query, (player_id,))
        status = cursor.fetchone()
        cursor.close()
        return status
        
    def get_player_location_info(self, player_id):
        """Obtém o ID da sala, nome da sala e descrição da sala atual do jogador."""
        cursor = self.conn.cursor()
        query = """
            SELECT s.id_sala, s.nome, s.descricao
            FROM Sala s
            JOIN Estagiario e ON s.id_sala = e.sala_atual
            WHERE e.id_personagem = %s;
        """
        cursor.execute(query, (player_id,))
        location_info = cursor.fetchone()
        cursor.close()
        return location_info

    def get_available_connections(self, sala_id):
        """Busca as conexões disponíveis a partir de uma sala."""
        cursor = self.conn.cursor()
        query = """
            SELECT cs.id_sala_destino, s.nome, 'Para', s.descricao
            FROM ConexaoSala cs
            JOIN Sala s ON cs.id_sala_destino = s.id_sala
            WHERE cs.id_sala_origem = %s;
        """
        cursor.execute(query, (sala_id,))
        connections = cursor.fetchall()
        cursor.close()
        return connections
    
    def move_player(self, player_id, sala_destino_id):
        """Move o jogador para uma nova sala e atualiza o andar."""
        try:
            cursor = self.conn.cursor()
            # Pega o id_andar da sala de destino
            cursor.execute("SELECT id_andar FROM Sala WHERE id_sala = %s", (sala_destino_id,))
            id_andar_destino = cursor.fetchone()[0]
            
            # Atualiza a sala e o andar do estagiário
            query = """
                UPDATE Estagiario
                SET sala_atual = %s, andar_atual = %s
                WHERE id_personagem = %s;
            """
            cursor.execute(query, (sala_destino_id, id_andar_destino, player_id))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao mover jogador: {e}", file=sys.stderr)
            return False

    def get_npcs_in_room(self, sala_id):
        """Retorna os NPCs presentes em uma determinada sala."""
        cursor = self.conn.cursor()
        # NPCs são associados a andares, mas podem aparecer em salas específicas para eventos.
        # Esta consulta busca NPCs no mesmo andar da sala.
        query = """
            SELECT p.id_personagem, p.nome, n.tipo
            FROM NPC n
            JOIN Personagem p ON n.id_personagem = p.id_personagem
            WHERE n.andar_atual = (SELECT id_andar FROM Sala WHERE id_sala = %s);
        """
        cursor.execute(query, (sala_id,))
        npcs = cursor.fetchall()
        cursor.close()
        return npcs
        
    def get_dialogue_for_npc(self, npc_id):
        """Busca uma linha de diálogo para um NPC."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT dialogo_padrao FROM NPC WHERE id_personagem = %s", (npc_id,))
        dialogue = cursor.fetchone()
        cursor.close()
        return dialogue[0] if dialogue else None
        
    def get_available_missions(self, player_id):
        """Lista missões principais disponíveis para o jogador."""
        cursor = self.conn.cursor()
        query = """
            SELECT 'Missao' AS tipo, m.nome, m.descricao, m.xp_recompensa
            FROM Missao m
            LEFT JOIN MissaoStatus ms ON m.id_missao = ms.id_missao AND ms.id_estagiario = %s
            LEFT JOIN MissaoConcluida mc ON m.id_missao = mc.id_missao AND mc.id_estagiario = %s
            WHERE (ms.status IS NULL OR ms.status = 'Disponível') 
            AND mc.id_missao IS NULL
            ORDER BY m.id_missao;
        """
        cursor.execute(query, (player_id, player_id))
        missions = cursor.fetchall()
        cursor.close()
        return missions
        
    def get_available_demands(self, player_id):
        """Lista demandas (sidequests) disponíveis para o jogador."""
        cursor = self.conn.cursor()
        query = """
            SELECT 'Demanda' AS tipo, d.nome, d.descricao, d.xp_recompensa, p.nome as solicitante
            FROM Demanda d
            JOIN NPC n ON d.id_npc = n.id_personagem
            JOIN Personagem p ON n.id_personagem = p.id_personagem
            LEFT JOIN DemandaConcluida dc ON d.id_demanda = dc.id_demanda AND dc.id_estagiario = %s
            WHERE dc.id_demanda IS NULL
            ORDER BY d.id_demanda;
        """
        cursor.execute(query, (player_id,))
        demands = cursor.fetchall()
        cursor.close()
        return demands
    
    def complete_mission(self, player_id, mission_id):
        """Marca uma missão como concluída e dá as recompensas."""
        try:
            cursor = self.conn.cursor()
            
            # Busca os dados da missão
            cursor.execute("SELECT xp_recompensa, moedas_recompensa FROM Missao WHERE id_missao = %s", (mission_id,))
            mission_data = cursor.fetchone()
            
            if not mission_data:
                return False, "Missão não encontrada"
            
            xp_reward, coins_reward = mission_data
            
            # Adiciona à tabela MissaoConcluida
            cursor.execute("""
                INSERT INTO MissaoConcluida (id_missao, id_estagiario, xp_ganho, moedas_ganhas)
                VALUES (%s, %s, %s, %s)
            """, (mission_id, player_id, xp_reward, coins_reward))
            
            # Atualiza status da missão para 'Concluída'
            cursor.execute("""
                INSERT INTO MissaoStatus (id_missao, id_estagiario, status)
                VALUES (%s, %s, 'Concluída')
                ON CONFLICT (id_missao, id_estagiario) 
                DO UPDATE SET status = 'Concluída'
            """, (mission_id, player_id))
            
            # Atualiza XP e moedas do jogador
            cursor.execute("""
                UPDATE Estagiario 
                SET xp = xp + %s, coins = coins + %s
                WHERE id_personagem = %s
            """, (xp_reward, coins_reward, player_id))
            
            self.conn.commit()
            cursor.close()
            return True, f"Missão concluída! +{xp_reward} XP, +{coins_reward} moedas"
            
        except Exception as e:
            self.conn.rollback()
            cursor.close()
            return False, f"Erro ao completar missão: {e}"
    
    def complete_demand(self, player_id, demand_id):
        """Marca uma demanda como concluída e dá as recompensas."""
        try:
            cursor = self.conn.cursor()
            
            # Busca os dados da demanda
            cursor.execute("SELECT xp_recompensa FROM Demanda WHERE id_demanda = %s", (demand_id,))
            demand_data = cursor.fetchone()
            
            if not demand_data:
                return False, "Demanda não encontrada"
            
            xp_reward = demand_data[0]
            
            # Adiciona à tabela DemandaConcluida
            cursor.execute("""
                INSERT INTO DemandaConcluida (id_demanda, id_estagiario)
                VALUES (%s, %s)
            """, (demand_id, player_id))
            
            # Atualiza XP do jogador
            cursor.execute("""
                UPDATE Estagiario 
                SET xp = xp + %s
                WHERE id_personagem = %s
            """, (xp_reward, player_id))
            
            self.conn.commit()
            cursor.close()
            return True, f"Demanda concluída! +{xp_reward} XP"
            
        except Exception as e:
            self.conn.rollback()
            cursor.close()
            return False, f"Erro ao completar demanda: {e}"