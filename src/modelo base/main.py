from control import DatabaseController
import interacoes
import sys

class TerminalInterface:
    def __init__(self, db_controller: DatabaseController):
        self.db_controller = db_controller
        self.current_player_id = None

    def run(self):
        """Inicia o menu principal do jogo."""
        while True:
            print("\n===== A SAGA DO ESTAGIÁRIO =====")
            print("1. Criar Novo Estagiário")
            print("2. Carregar Jogo")
            print("3. Executar Scripts de Configuração (DDL/DML)")
            print("4. Sair")
            choice = input("Escolha uma opção: ").strip()

            if choice == "1":
                self.add_new_player()
            elif choice == "2":
                self.select_player_and_start_game()
            elif choice == "3":
                self.run_initial_scripts()
            elif choice == "4":
                print("Até a próxima! Não se atrase para o trabalho.")
                sys.exit(0)
            else:
                print("Opção inválida, tente novamente.")

    def add_new_player(self):
        """Cria um novo personagem jogador."""
        nome_jogador = input("Digite o nome do seu estagiário: ").strip()
        if nome_jogador:
            self.db_controller.connect()
            self.db_controller.add_estagiario(nome_jogador)
            self.db_controller.close()
        else:
            print("O nome não pode ser vazio.")

    def select_player_and_start_game(self):
        """Seleciona um jogador existente e inicia o jogo."""
        self.db_controller.connect()
        jogadores = self.db_controller.get_registered_players()
        self.db_controller.close()

        if not jogadores:
            print("\nNenhum estagiário cadastrado. Crie um primeiro.")
            return

        print("\nEscolha seu estagiário para continuar a jornada:")
        for (pid, nome) in jogadores:
            print(f"{pid}. {nome}")
        
        try:
            choice = int(input("Digite o número do estagiário: ").strip())
            if any(p[0] == choice for p in jogadores):
                self.current_player_id = choice
                nome_jogador = [p[1] for p in jogadores if p[0] == choice][0]
                print(f"\nBem-vindo de volta, {nome_jogador}! A labuta continua...")
                self.game_loop()
            else:
                print("ID inválido.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")

    def run_initial_scripts(self):
        """Executa os scripts DDL e DML para configurar o banco de dados."""
        print("\nEsta ação irá criar/recriar as tabelas e dados iniciais.")
        confirm = input("Tem certeza que deseja continuar? (s/n): ").strip().lower()
        if confirm == 's':
            try:
                self.db_controller.connect()
                print("Executando DDL.sql...")
                self.db_controller.execute_sql_script('DDL.sql')
                print("Executando DML.sql...")
                self.db_controller.execute_sql_script('DML.sql')
                self.db_controller.close()
                print("\nBanco de dados configurado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro durante a execução dos scripts: {e}")
        else:
            print("Operação cancelada.")


    def game_loop(self):
        """O loop principal do jogo onde as ações do jogador acontecem."""
        while self.current_player_id is not None:
            self.db_controller.connect()
            location_info = self.db_controller.get_player_location_info(self.current_player_id)
            self.db_controller.close()

            print(f"\n--- Você está em: {location_info[1]} ---")
            print("O que você faz agora?")
            print("1. Olhar ao redor")
            print("2. Mover-se")
            print("3. Ver meu status")
            print("4. Ver tarefas (Missões e Demandas)")
            print("5. Falar com alguém")
            print("6. Deslogar (Sair para o menu principal)")

            choice = input("> ").strip()
            
            self.db_controller.connect()
            if choice == "1":
                interacoes.explorar_sala(self.db_controller, self.current_player_id)
            elif choice == "2":
                self.move_player()
            elif choice == "3":
                interacoes.exibir_status_jogador(self.db_controller, self.current_player_id)
            elif choice == "4":
                interacoes.exibir_missoes_e_demandas(self.db_controller, self.current_player_id)
            elif choice == "5":
                interacoes.conversar_com_npc(self.db_controller, self.current_player_id)
            elif choice == "6":
                print("Fazendo logoff... Até mais!")
                self.current_player_id = None
            else:
                print("Comando desconhecido. (Digite um número de 1 a 6)")
            self.db_controller.close()

    def move_player(self):
        """Lida com a lógica de movimentação do jogador."""
        id_sala_atual, _, _ = self.db_controller.get_player_location_info(self.current_player_id)
        conexoes = self.db_controller.get_available_connections(id_sala_atual)

        if not conexoes:
            print("Você não vê nenhuma saída óbvia desta sala.")
            return

        print("\nVocê pode ir para:")
        for i, (id_destino, nome_destino, direcao, desc) in enumerate(conexoes):
            print(f"{i + 1}. {nome_destino} ({direcao}) - {desc}")
        print("0. Ficar onde estou")

        try:
            choice = int(input("Para onde ir? ").strip())
            if choice == 0:
                return
            if 1 <= choice <= len(conexoes):
                id_sala_destino = conexoes[choice - 1][0]
                if self.db_controller.move_player(self.current_player_id, id_sala_destino):
                    print("Você se move para a nova sala.")
                    # Chama explorar sala para dar feedback imediato do novo local
                    interacoes.explorar_sala(self.db_controller, self.current_player_id)
            else:
                print("Opção inválida.")
        except ValueError:
            print("Por favor, digite um número.")


if __name__ == "__main__":
    # Certifique-se de que as credenciais do banco de dados estão corretas
    db_controller = DatabaseController(
        dbname="saga_estagiario_db", 
        user="postgres",  # Mude para seu usuário, se necessário
        password="admin", # Mude para sua senha
        host="localhost",
        port="5432"
    )
    terminal_interface = TerminalInterface(db_controller)
    terminal_interface.run()