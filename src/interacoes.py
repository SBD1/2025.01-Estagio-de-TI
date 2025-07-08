import time
import random

# MODIFICAÇÃO 1: Importar as novas funções de interação com itens
from database import (
    get_npcs_in_room,
    get_player_missions_status,
    accept_mission,
    complete_mission,
    get_player_missions,
    get_player_stats,
    get_inimigos_na_sala,
    get_missao_combate_ativa,
    atualizar_progresso_combate,
    get_player_inventory,
    use_item,      # Adicionado
    equip_item,    # Adicionado
    unequip_item   # Adicionado
)
from dialogos import DIALOGOS

def _print_dialogue(npc_name, dialogue_lines):
    """Função auxiliar para imprimir diálogos com pausas."""
    if isinstance(dialogue_lines, str):
        dialogue_lines = [dialogue_lines]
    
    for line in dialogue_lines:
        print(f"\n[{npc_name}]: \"{line}\"")
        time.sleep(1.5)

def conversar_com_npc(player_id, sala_id):
    """Lida com a lógica de conversa com NPCs usando o sistema de diálogos."""
    npcs = get_npcs_in_room(sala_id)
    if not npcs:
        print("Não há ninguém para conversar aqui.")
        time.sleep(2)
        return

    print("\nCom quem você gostaria de falar?")
    for i, (id_npc, nome_npc, _) in enumerate(npcs, 1):
        print(f"  [{i}] {nome_npc}")
    print("  [0] Voltar")

    try:
        choice = int(input("> ").strip())
        if choice == 0: return
        
        if 1 <= choice <= len(npcs):
            id_npc, nome_npc, _ = npcs[choice - 1]
            
            npc_script = DIALOGOS.get(id_npc)
            if not npc_script:
                print(f"\n[{nome_npc}]: \"...\" (Este personagem parece não ter muito a dizer agora).")
                input("\nPressione Enter para continuar...")
                return

            player_missions = get_player_missions_status(player_id)
            
            mission_in_progress_id = None
            available_mission_id = None

            for mission_id in npc_script.get('missao_em_andamento', {}):
                if player_missions.get(mission_id) == 'Em Andamento':
                    mission_in_progress_id = mission_id
                    break
            
            if not mission_in_progress_id:
                for mission_id in npc_script.get('missao_disponivel', {}):
                    if player_missions.get(mission_id) is None:
                        available_mission_id = mission_id
                        break

            if player_missions.get(8) == 'Em Andamento' and 'missao_alvo' in npc_script:
                _print_dialogue(nome_npc, npc_script['missao_alvo'])
                print("\n(Você recuperou o Pão de Queijo!)")
                message = complete_mission(player_id, 8)
                print(message)
                input("\nPressione Enter para continuar...")

            elif mission_in_progress_id:
                dialogo = npc_script['missao_em_andamento'][mission_in_progress_id]
                _print_dialogue(nome_npc, dialogo)
                input("\nPressione Enter para continuar...")

            elif available_mission_id:
                dialogo = npc_script['missao_disponivel'][available_mission_id]
                _print_dialogue(nome_npc, dialogo)
                
                confirm = input(f"Aceitar a missão? (s/n): ").lower()
                if confirm == 's':
                    success, message = accept_mission(player_id, available_mission_id)
                    print(message)
                    time.sleep(2)

            else:
                dialogo = npc_script.get('padrao', "...")
                _print_dialogue(nome_npc, dialogo)
                input("\nPressione Enter para continuar...")

    except ValueError:
        print("Entrada inválida.")
        time.sleep(2)

def interagir_com_ambiente(player_id, mission_info):
    """Lida com a lógica de interação com o ambiente para completar missões."""
    mission_id, mission_name, mission_type = mission_info
    
    if mission_type == 'Manutenção' and mission_name == 'Check-up no Servidor':
        print("\nVocê se aproxima do servidor superaquecido...")
        time.sleep(1.5)
        print("Com cuidado, você desliga, limpa os coolers e reinicia o sistema.")
        time.sleep(2)
        print("A temperatura volta ao normal. Ótimo trabalho!")
        
        message = complete_mission(player_id, mission_id)
        print(f"\n{message}")
        input("\nPressione Enter para continuar...")
    else:
        print("Não há nada de interessante para interagir aqui no momento.")
        time.sleep(2)

def exibir_missoes_e_demandas(player_id):
    """Exibe as missões ativas e concluídas do jogador."""
    missions = get_player_missions(player_id)
    
    print("\n--- SEU PAINEL DE TAREFAS ---")
    if not missions:
        print("Você não tem nenhuma tarefa no momento. Explore e converse com as pessoas!")
    else:
        print("\n-- Em Andamento --")
        em_andamento = False
        for nome, status, desc in missions:
            if status == 'Em Andamento':
                print(f"\n- {nome} [{status}]")
                print(f"  Descrição: {desc}")
                em_andamento = True
        if not em_andamento:
            print("Nenhuma missão em andamento.")

        print("\n-- Concluídas --")
        concluidas = False
        for nome, status, desc in missions:
            if status == 'Concluída':
                print(f"- {nome}")
                concluidas = True
        if not concluidas:
            print("Nenhuma missão concluída ainda.")
    
    print("\n" + "="*30)
    input("Pressione Enter para voltar...")

def iniciar_combate(player_id, sala_id):
    """Inicia e gerencia um loop de combate contra inimigos na sala."""
    inimigos = get_inimigos_na_sala(sala_id)
    if not inimigos:
        print("\nNão há ameaças aqui. Você respira aliviado.")
        time.sleep(2)
        return

    print("\nALERTA! Inimigos se aproximam!")
    time.sleep(1)

    for id_instancia, nome_inimigo, vida_inimigo, dano_inimigo, mission_id in inimigos:
        print(f"\n--- Você enfrenta um(a) {nome_inimigo}! ---")
        
        player_stats = get_player_stats(player_id)
        if not player_stats:
            print("Erro: não foi possível carregar os dados do jogador para o combate.")
            return
            
        # Os índices mudaram devido à nova query em get_player_stats
        vida_jogador = player_stats[7]
        ataque_jogador = player_stats[5]
        defesa_jogador = player_stats[6]

        while vida_inimigo > 0 and vida_jogador > 0:
            print(f"\nSua Vida: {vida_jogador} | Vida do {nome_inimigo}: {vida_inimigo}")
            print("Escolha sua ação:")
            print("  [1] Atacar")
            print("  [2] Tentar Fugir")
            
            escolha = input("> ").strip()

            if escolha == '1':
                dano_causado = max(1, ataque_jogador + random.randint(-2, 5))
                vida_inimigo -= dano_causado
                print(f"Você ataca e causa {dano_causado} de dano ao {nome_inimigo}.")
                time.sleep(1)

                if vida_inimigo <= 0:
                    print(f"\nVocê derrotou o(a) {nome_inimigo}!")
                    
                    atualizar_progresso_combate(mission_id) 
                    progresso = get_missao_combate_ativa(player_id, mission_id)
                    
                    if progresso:
                        alvo, atual = progresso
                        print(f"Progresso da missão: {atual}/{alvo}")
                        if atual >= alvo:
                            print("\nObjetivo da missão de combate alcançado!")
                            mensagem_conclusao = complete_mission(player_id, mission_id)
                            print(mensagem_conclusao)
                    
                    time.sleep(2)
                    break 

                dano_recebido = max(1, dano_inimigo - defesa_jogador + random.randint(-3, 3))
                vida_jogador -= dano_recebido
                print(f"O {nome_inimigo} contra-ataca e você recebe {dano_recebido} de dano.")
                time.sleep(1)

                if vida_jogador <= 0:
                    print("\nVocê foi derrotado! Você desmaia e acorda na recepção, um pouco tonto...")
                    time.sleep(3)
                    return

            elif escolha == '2':
                if random.random() > 0.5:
                    print("Você conseguiu fugir!")
                    time.sleep(2)
                    return
                else:
                    print("A fuga falhou! Você perde a sua vez.")
                    dano_recebido = max(1, dano_inimigo - defesa_jogador)
                    vida_jogador -= dano_recebido
                    print(f"O {nome_inimigo} ataca enquanto você tentava fugir, causando {dano_recebido} de dano.")
                    time.sleep(1)
            else:
                print("Ação inválida. Você hesita e perde a vez.")
                time.sleep(1)

    print("\nTodos os inimigos na sala foram derrotados. A área está segura.")
    time.sleep(2)

# MODIFICAÇÃO 2: A função de exibir inventário foi substituída por uma função de gerenciamento interativo.
def gerenciar_inventario(personagem_id):
    """Exibe o inventário do jogador e permite interagir com os itens."""
    while True:
        print("\n=== SUA MOCHILA E EQUIPAMENTOS ===\n")
        # A função get_player_inventory agora retorna mais colunas
        items = get_player_inventory(personagem_id)

        if not items:
            print("Você não tem nenhum item. Hora de conseguir alguns!")
            input("\nPressione Enter para continuar...")
            return

        # Mapeia o índice da lista para o ID da instância do item para fácil seleção
        item_map = {}
        for idx, (id_instancia, nome, quantidade, descricao, tipo, status) in enumerate(items, 1):
            item_map[idx] = (id_instancia, tipo, status)
            print(f" [{idx}] {nome} (x{quantidade}) - [{status}]")
            print(f"       ↳ {descricao}\n")

        print(" [0] Voltar")
        print("\n----------------------------------")

        try:
            escolha_str = input("Selecione um item para interagir (ou 0 para sair): ").strip()
            if not escolha_str or escolha_str == "0":
                return

            escolha = int(escolha_str)
            if escolha in item_map:
                id_instancia, tipo, status = item_map[escolha]
                mensagem = ""

                # Lógica para itens consumíveis ou power-ups que estão na mochila
                if tipo in ['Consumivel', 'PowerUp'] and 'Equipado' not in status:
                    confirm = input(f"Deseja usar '{items[escolha-1][1]}'? (s/n): ").lower()
                    if confirm == 's':
                        mensagem = use_item(personagem_id, id_instancia)

                # Lógica para equipamentos
                elif tipo == 'Equipamento':
                    if 'Equipado' in status:
                        confirm = input(f"Deseja desequipar '{items[escolha-1][1]}'? (s/n): ").lower()
                        if confirm == 's':
                            mensagem = unequip_item(personagem_id, id_instancia)
                    else:
                        confirm = input(f"Deseja equipar '{items[escolha-1][1]}'? (s/n): ").lower()
                        if confirm == 's':
                            mensagem = equip_item(personagem_id, id_instancia)
                else:
                    print("\nNão há ação disponível para este item no momento.")
                    time.sleep(2)


                if mensagem:
                    print(f"\n{mensagem}")
                    time.sleep(2.5)

            else:
                print("Opção inválida.")
                time.sleep(2)

        except (ValueError):
            print("Entrada inválida. Por favor, digite um número.")
            time.sleep(2)