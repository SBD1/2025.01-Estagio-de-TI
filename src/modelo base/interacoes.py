import time

def type_print(text, delay=0.03):
    """Imprime o texto com um efeito de digitação."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def exibir_status_jogador(db_controller, player_id):
    """Busca e exibe o status formatado do jogador."""
    status = db_controller.get_player_status(player_id)
    if status:
        nome, nivel, xp, coins, p_status, sala, andar = status
        print("\n" + "="*30)
        type_print(f"FICHA DO ESTAGIÁRIO".center(30))
        print("="*30)
        print(f"Nome: {nome}")
        print(f"Nível: {nivel}")
        print(f"XP: {xp}")
        print(f"Coins: {coins} C$")
        print(f"Status: {p_status}")
        print(f"Local: {sala} ({andar})")
        print("="*30 + "\n")
    else:
        print("Não foi possível encontrar os dados do jogador.")

def explorar_sala(db_controller, player_id):
    """Descreve a sala atual e os NPCs presentes."""
    location_info = db_controller.get_player_location_info(player_id)
    if not location_info:
        print("Você parece estar perdido no limbo...")
        return

    id_sala, nome_sala, desc_sala = location_info
    
    type_print(f"\nVocê está em: {nome_sala}")
    type_print(f" > {desc_sala}")

    npcs_na_sala = db_controller.get_npcs_in_room(id_sala)
    if npcs_na_sala:
        print("\nVocê vê algumas pessoas por aqui:")
        for _, nome_npc, funcao_npc in npcs_na_sala:
            print(f"- {nome_npc} ({funcao_npc})")
    else:
        print("\nA sala parece vazia no momento.")

def conversar_com_npc(db_controller, player_id):
    """Permite ao jogador iniciar uma conversa com um NPC na sala."""
    id_sala, _, _ = db_controller.get_player_location_info(player_id)
    npcs = db_controller.get_npcs_in_room(id_sala)

    if not npcs:
        print("Não há com quem conversar aqui.")
        return

    print("\nCom quem você gostaria de falar?")
    for i, (id_npc, nome_npc, _) in enumerate(npcs):
        print(f"{i + 1}. {nome_npc}")
    print("0. Voltar")

    try:
        choice = int(input("Escolha uma opção: ").strip())
        if choice == 0:
            return
        if 1 <= choice <= len(npcs):
            id_npc_escolhido, nome_npc_escolhido, _ = npcs[choice - 1]
            dialogo = db_controller.get_dialogue_for_npc(id_npc_escolhido)
            if dialogo:
                type_print(f"\n[{nome_npc_escolhido}]: \"{dialogo}\"")
            else:
                type_print(f"\n[{nome_npc_escolhido}] parece ocupado(a) e não diz nada.")
            # Aqui poderia ser expandido para oferecer missões/demandas do NPC
        else:
            print("Opção inválida.")
    except ValueError:
        print("Por favor, digite um número.")

def exibir_missoes_e_demandas(db_controller, player_id):
    """Exibe as missões e demandas disponíveis para o jogador."""
    missoes = db_controller.get_available_missions(player_id)
    demandas = db_controller.get_available_demands(player_id)

    print("\n" + "="*40)
    type_print("PAINEL DE TAREFAS".center(40))
    print("="*40)

    if not missoes and not demandas:
        print("Você está em dia com suas tarefas. Hora do café?")
        return

    if missoes:
        print("\n--- MISSÕES PRINCIPAIS ---")
        for tipo, nome, desc, xp in missoes:
            print(f"\n- {nome} ({tipo})")
            print(f"  Descrição: {desc}")
            print(f"  Recompensa: {xp} XP")
    
    if demandas:
        print("\n--- DEMANDAS (SIDEQUESTS) ---")
        for tipo, nome, desc, xp, solicitante in demandas:
            print(f"\n- {nome} ({tipo})")
            print(f"  Solicitante: {solicitante}")
            print(f"  Descrição: {desc}")
            print(f"  Recompensa: {xp} XP")
    
    print("\n" + "="*40)