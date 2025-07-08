import os
import time
from database import (
    call_db_function, get_all_characters, get_location_details,
    get_available_missions, accept_mission, get_mission_details, complete_mission,
    get_player_inventory, get_npcs_in_location, get_enemies_in_location,
    attack_enemy, check_mission_completion, update_combat_mission_progress,
    get_player_status, get_player_achievements, check_and_grant_achievements,
    complete_delivery_mission, get_mission_progress, update_player_name,
    check_and_complete_missions
)

def clear_screen():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_personagem():
    """Lida com a lógica de criação de personagem."""
    clear_screen()
    print("--- CRIAÇÃO DE PERSONAGEM ---\n")
    nome = input("Digite o nome do seu personagem: ").strip()

    if not nome:
        print("\nO nome não pode ser vazio. Tente novamente.")
        time.sleep(2)
        return

    # Chama a função SQL para criar o personagem
    mensagem = call_db_function('criar_personagem', nome)
    print(f"\n{mensagem}")
    time.sleep(3)

def iniciar_jogo():
    """Lida com a seleção de personagem e o início do loop do jogo."""
    clear_screen()
    print("--- INICIAR JOGO ---\n")
    print("Selecione um personagem para continuar:\n")

    personagens = get_all_characters()

    if not personagens:
        print("Nenhum personagem criado ainda.")
        print("Por favor, crie um personagem no menu principal primeiro.")
        time.sleep(3)
        return

    for char_id, char_name in personagens:
        print(f"[{char_id}] - {char_name}")

    try:
        escolha = int(input("\nDigite o ID do personagem: "))
        # Verifica se a escolha é um ID válido
        personagem_selecionado = next((p for p in personagens if p[0] == escolha), None)

        if not personagem_selecionado:
            raise ValueError

        game_loop(personagem_selecionado[0], personagem_selecionado[1])

    except (ValueError, IndexError):
        print("\nOpção inválida. Retornando ao menu principal.")
        time.sleep(2)

def alterar_nome_personagem(personagem_id):
    """Permite alterar o nome do personagem."""
    clear_screen()
    print("--- ALTERAR NOME DO PERSONAGEM ---\n")
    
    # Mostra nome atual
    status = get_player_status(personagem_id)
    if status:
        nome_atual = status[0]
        print(f"Nome atual: {nome_atual}")
    
    novo_nome = input("\nDigite o novo nome (ou Enter para cancelar): ").strip()
    
    if not novo_nome:
        print("Operação cancelada.")
        time.sleep(2)
        return
    
    if update_player_name(personagem_id, novo_nome):
        print(f"\n✅ Nome alterado com sucesso para: {novo_nome}")
    else:
        print("\n❌ Erro ao alterar nome.")
    
    time.sleep(2)

def exibir_status_jogador(personagem_id):
    """Exibe o status completo do jogador."""
    clear_screen()
    print("--- STATUS DO JOGADOR ---\n")
    
    status = get_player_status(personagem_id)
    
    if status:
        nome, nivel, xp, coins, p_status, andar_nome, sala_nome = status
        print(f"Nome: {nome}")
        print(f"Nível: {nivel}")
        print(f"XP: {xp}")
        print(f"Moedas: {coins}")
        print(f"Status: {p_status}")
        print(f"Localização: {sala_nome}, {andar_nome}")
        
        # Calcula XP para próximo nível
        xp_proximo_nivel = (nivel * 100) - xp
        if xp_proximo_nivel > 0:
            print(f"XP para próximo nível: {xp_proximo_nivel}")
        else:
            print("Pronto para subir de nível!")
    else:
        print("Erro ao carregar status do jogador.")
    
    # Verifica conquistas
    conquistas_msg = check_and_grant_achievements(personagem_id)
    if "Conquista desbloqueada" in conquistas_msg:
        print(f"\n🎉 {conquistas_msg}")
    
    print("\nOpções:")
    print("[1] Alterar nome")
    print("[2] Voltar")
    
    try:
        escolha = int(input("\nSua escolha: "))
        if escolha == 1:
            alterar_nome_personagem(personagem_id)
        elif escolha == 2:
            return
    except ValueError:
        print("Opção inválida.")
        time.sleep(2)

def exibir_conquistas(personagem_id):
    """Exibe as conquistas do jogador."""
    clear_screen()
    print("--- CONQUISTAS ---\n")
    
    achievements = get_player_achievements(personagem_id)
    
    if not achievements:
        print("Você ainda não desbloqueou nenhuma conquista.")
        print("Complete missões e explore o mundo para desbloquear conquistas!")
    else:
        print("Suas conquistas:")
        for i, (nome, descricao, data) in enumerate(achievements, 1):
            data_formatada = data.strftime("%d/%m/%Y %H:%M")
            print(f"\n🏆 {nome}")
            print(f"   {descricao}")
            print(f"   Desbloqueada em: {data_formatada}")
    
    input("\nPressione Enter para continuar...")

def exibir_missoes(personagem_id):
    """Exibe as missões disponíveis e em andamento."""
    clear_screen()
    print("--- MISSÕES ---\n")
    
    missions = get_available_missions(personagem_id)
    
    if not missions:
        print("Nenhuma missão disponível no momento.")
        input("\nPressione Enter para continuar...")
        return
    
    print("Missões disponíveis:")
    for i, (id_missao, nome, descricao, tipo, xp, moedas, status) in enumerate(missions, 1):
        status_color = "🟢" if status == "Disponível" else "🟡" if status == "Em Andamento" else "🔴"
        print(f"\n[{i}] {status_color} {nome} ({tipo})")
        print(f"    {descricao}")
        print(f"    Recompensa: {xp} XP, {moedas} moedas")
        print(f"    Status: {status}")
        
        # Mostra progresso se em andamento
        if status == "Em Andamento":
            progress = get_mission_progress(personagem_id, id_missao)
            if progress:
                print(f"    {progress}")
    
    print(f"\n[{len(missions) + 1}] Voltar")
    
    try:
        escolha = int(input("\nEscolha uma missão para mais detalhes: "))
        if 1 <= escolha <= len(missions):
            mission_data = missions[escolha - 1]
            gerenciar_missao(personagem_id, mission_data)
        elif escolha == len(missions) + 1:
            return
        else:
            print("Opção inválida.")
            time.sleep(2)
    except ValueError:
        print("Por favor, digite um número válido.")
        time.sleep(2)

def gerenciar_missao(personagem_id, mission_data):
    """Gerencia uma missão específica."""
    id_missao, nome, descricao, tipo, xp, moedas, status = mission_data
    
    clear_screen()
    print(f"--- {nome} ---\n")
    
    # Busca detalhes completos da missão
    details = get_mission_details(id_missao)
    if details:
        _, _, full_desc, dialogo_inicial, _, _, _, _ = details
        print(f"Tipo: {tipo}")
        print(f"Descrição: {full_desc}")
        print(f"Diálogo inicial: \"{dialogo_inicial}\"")
        print(f"Recompensa: {xp} XP, {moedas} moedas")
        print(f"Status atual: {status}")
        
        # Mostra progresso se em andamento
        if status == "Em Andamento":
            progress = get_mission_progress(personagem_id, id_missao)
            if progress:
                print(f"Progresso: {progress}")
    
    print("\nOpções:")
    
    if status == "Disponível":
        print("[1] Aceitar Missão")
        print("[2] Voltar")
        
        try:
            escolha = int(input("\nSua escolha: "))
            if escolha == 1:
                if accept_mission(personagem_id, id_missao):
                    print("\nMissão aceita! Boa sorte!")
                    time.sleep(2)
                else:
                    print("\nErro ao aceitar missão.")
                    time.sleep(2)
            elif escolha == 2:
                return
        except ValueError:
            print("Opção inválida.")
            time.sleep(2)
    
    elif status == "Em Andamento":
        print("[1] Verificar se pode completar")
        print("[2] Voltar")
        
        try:
            escolha = int(input("\nSua escolha: "))
            if escolha == 1:
                if check_mission_completion(personagem_id, id_missao):
                    print("\nMissão pronta para conclusão!")
                    confirmar = input("Deseja completar a missão? (s/n): ").strip().lower()
                    if confirmar == 's':
                        # Trata missões de entrega especialmente
                        if tipo == "Entrega":
                            success, message = complete_delivery_mission(personagem_id, id_missao)
                            if success:
                                if complete_mission(personagem_id, id_missao):
                                    print(f"\n{message}")
                                    print(f"Missão completada! +{xp} XP, +{moedas} moedas!")
                                    
                                    # Verifica conquistas
                                    conquistas_msg = check_and_grant_achievements(personagem_id)
                                    if "Conquista desbloqueada" in conquistas_msg:
                                        print(f"\n🎉 {conquistas_msg}")
                                    
                                    time.sleep(4)
                                else:
                                    print("\nErro ao completar missão.")
                                    time.sleep(2)
                            else:
                                print(f"\n{message}")
                                time.sleep(3)
                        else:
                            if complete_mission(personagem_id, id_missao):
                                print(f"\nMissão completada! +{xp} XP, +{moedas} moedas!")
                                
                                # Verifica conquistas
                                conquistas_msg = check_and_grant_achievements(personagem_id)
                                if "Conquista desbloqueada" in conquistas_msg:
                                    print(f"\n🎉 {conquistas_msg}")
                                
                                time.sleep(4)
                            else:
                                print("\nErro ao completar missão.")
                                time.sleep(2)
                else:
                    print("\nVocê ainda não cumpriu os requisitos da missão.")
                    if tipo == "Combate":
                        print("Dica: Procure por inimigos e derrote-os!")
                    elif tipo == "Entrega":
                        print("Dica: Verifique se tem o item necessário no inventário.")
                    elif tipo == "Conversa":
                        print("Dica: Fale com o NPC correto.")
                    time.sleep(3)
            elif escolha == 2:
                return
        except ValueError:
            print("Opção inválida.")
            time.sleep(2)

def exibir_inventario(personagem_id):
    """Exibe o inventário do jogador."""
    clear_screen()
    print("--- INVENTÁRIO ---\n")
    
    items = get_player_inventory(personagem_id)
    
    if not items:
        print("Seu inventário está vazio.")
    else:
        print("Itens no inventário:")
        for item_id, nome, descricao, quantidade in items:
            print(f"\n• {nome} (x{quantidade})")
            print(f"  {descricao}")
    
    input("\nPressione Enter para continuar...")

def interagir_com_npcs(personagem_id):
    """Permite interagir com NPCs na localização atual."""
    clear_screen()
    print("--- INTERAÇÃO COM NPCs ---\n")
    
    npcs = get_npcs_in_location(personagem_id)
    
    if not npcs:
        print("Não há NPCs por aqui.")
        input("\nPressione Enter para continuar...")
        return
    
    print("NPCs disponíveis:")
    for i, (npc_id, nome, tipo, dialogo) in enumerate(npcs, 1):
        print(f"[{i}] {nome} ({tipo})")
    
    print(f"[{len(npcs) + 1}] Voltar")
    
    try:
        escolha = int(input("\nCom quem deseja falar? "))
        if 1 <= escolha <= len(npcs):
            npc_data = npcs[escolha - 1]
            npc_id, nome, tipo, dialogo = npc_data
            
            clear_screen()
            print(f"--- Conversando com {nome} ---\n")
            print(f"[{nome}]: \"{dialogo}\"")
            
            input("\nPressione Enter para continuar...")
        elif escolha == len(npcs) + 1:
            return
        else:
            print("Opção inválida.")
            time.sleep(2)
    except ValueError:
        print("Por favor, digite um número válido.")
        time.sleep(2)

def iniciar_combate(personagem_id):
    """Inicia sistema de combate contínuo."""
    while True:
        clear_screen()
        print("--- ARENA DE COMBATE ---\n")
        
        enemies = get_enemies_in_location(personagem_id)
        
        if not enemies:
            print("🏆 Não há mais inimigos por aqui!")
            print("Parabéns, você limpou a área!")
            input("\nPressione Enter para voltar...")
            return
        
        print("Inimigos disponíveis:")
        for i, (inst_id, nome, vida, dano, ataque) in enumerate(enemies, 1):
            status_vida = "🟢" if vida > 70 else "🟡" if vida > 30 else "🔴"
            print(f"[{i}] {status_vida} {nome} (HP: {vida}, Ataque: {ataque})")
        
        print(f"\n[{len(enemies) + 1}] 🚪 Sair da arena")
        
        try:
            escolha = int(input("\nQual inimigo deseja atacar? "))
            if 1 <= escolha <= len(enemies):
                enemy_data = enemies[escolha - 1]
                inst_id, nome, vida, dano, ataque = enemy_data
                
                print(f"\n⚔️ COMBATE CONTRA {nome.upper()}!")
                print("-" * 50)
                
                # Loop de combate individual
                while True:
                    print(f"\n🎯 {nome} (HP: {vida})")
                    print("Opções:")
                    print("[1] ⚔️  Atacar")
                    print("[2] 🏃 Fugir do combate")
                    
                    try:
                        acao = int(input("\nSua ação: "))
                        if acao == 1:
                            success, message = attack_enemy(personagem_id, inst_id)
                            print(f"\n{message}")
                            
                            if success and "derrotado" in message:
                                print("\n🎉 Vitória!")
                                
                                # Verifica conquistas
                                conquistas_msg = check_and_grant_achievements(personagem_id)
                                if "Conquista desbloqueada" in conquistas_msg:
                                    print(f"🎉 {conquistas_msg}")
                                
                                input("\nPressione Enter para continuar na arena...")
                                break  # Sai do loop individual, volta para seleção de inimigos
                            
                            elif not success:
                                print("❌ Erro no combate!")
                                input("Pressione Enter para tentar novamente...")
                            
                            else:
                                # Inimigo ainda vivo, continua o combate
                                # Atualiza a vida do inimigo para o próximo turno
                                enemies = get_enemies_in_location(personagem_id)
                                enemy_found = False
                                for enemy in enemies:
                                    if enemy[0] == inst_id:
                                        vida = enemy[2]  # Atualiza HP
                                        enemy_found = True
                                        break
                                
                                if not enemy_found or vida <= 0:
                                    print("💀 Inimigo foi derrotado!")
                                    break
                                
                                input("\nPressione Enter para próximo turno...")
                        
                        elif acao == 2:
                            print("🏃 Você fugiu do combate!")
                            time.sleep(1)
                            break  # Volta para seleção de inimigos
                        
                        else:
                            print("❌ Ação inválida!")
                            time.sleep(1)
                    
                    except ValueError:
                        print("❌ Digite um número válido!")
                        time.sleep(1)
            
            elif escolha == len(enemies) + 1:
                print("🚪 Saindo da arena...")
                return
            
            else:
                print("❌ Opção inválida!")
                time.sleep(1)
        
        except ValueError:
            print("❌ Por favor, digite um número válido!")
            time.sleep(1)

def game_loop(personagem_id, personagem_nome):
    """O loop principal do jogo, com menu de opções numérico."""
    clear_screen()
    print(f"Iniciando o jogo com {personagem_nome}...")
    time.sleep(2)

    while True:
        clear_screen()
        
        # 1. Pega os detalhes estruturados do local atual
        location_details = get_location_details(personagem_id)

        if not location_details:
            print("Erro ao carregar o local. Voltando ao menu.")
            time.sleep(3)
            break
        
        nome_sala, descricao_sala, saidas_disponiveis = location_details

        # 2. Exibe as informações do local
        print(f"--- {personagem_nome} ---")
        print(f"Você está no: {nome_sala}")
        print(descricao_sala)
        print("\n" + "="*50)
        print("O que você faz?\n")

        # 3. Menu principal de opções
        print("  [1] Mover-se")
        print("  [2] Ver Missões")
        print("  [3] Ver Inventário")
        print("  [4] Falar com NPCs")
        print("  [5] Combater")
        print("  [6] Ver Status")
        print("  [7] Ver Conquistas")
        print("  [8] Voltar ao menu principal")
        print("\n" + "="*50)

        # 4. Pega e processa a escolha do jogador
        try:
            escolha_str = input("Sua escolha: ").strip()
            if not escolha_str: continue # Se o usuário só apertar Enter, repete o loop

            escolha_num = int(escolha_str)
            
            if escolha_num == 1:
                # Submenu de movimento
                clear_screen()
                print(f"--- Movimentação ---\n")
                print("Para onde deseja ir?")
                
                # Garante que 'saidas_disponiveis' não seja None
                saidas_disponiveis = saidas_disponiveis or []
                
                for i, saida in enumerate(saidas_disponiveis, start=1):
                    print(f"  [{i}] {saida}")
                
                print(f"  [{len(saidas_disponiveis) + 1}] Cancelar")
                
                try:
                    mov_escolha = int(input("\nSua escolha: "))
                    if 1 <= mov_escolha <= len(saidas_disponiveis):
                        direcao_escolhida = saidas_disponiveis[mov_escolha - 1]
                        print(f"\nTentando: {direcao_escolhida}...")
                        call_db_function('mover_personagem', personagem_id, direcao_escolhida)
                        time.sleep(1)
                    elif mov_escolha == len(saidas_disponiveis) + 1:
                        continue
                    else:
                        print("Opção inválida.")
                        time.sleep(2)
                except ValueError:
                    print("Por favor, digite um número válido.")
                    time.sleep(2)
            
            elif escolha_num == 2:
                exibir_missoes(personagem_id)
            
            elif escolha_num == 3:
                exibir_inventario(personagem_id)
            
            elif escolha_num == 4:
                interagir_com_npcs(personagem_id)
            
            elif escolha_num == 5:
                iniciar_combate(personagem_id)
            
            elif escolha_num == 6:
                exibir_status_jogador(personagem_id)
            
            elif escolha_num == 7:
                exibir_conquistas(personagem_id)
            
            elif escolha_num == 8:
                print("\nVoltando ao menu principal...")
                time.sleep(2)
                break
            
            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(2)

        except ValueError:
            print("\nPor favor, digite um número. Tente novamente.")
            time.sleep(2)

def main_menu():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        clear_screen()
        print("========================================")
        print("      BEM-VINDO AO JOGO DE TERMINAL     ")
        print("========================================")
        print("\nEscolha uma opção:")
        print("  [1] Criar Novo Personagem")
        print("  [2] Iniciar Jogo")
        print("  [3] Sair")
        print("\n----------------------------------------")

        escolha = input("Sua escolha: ").strip()

        if escolha == '1':
            criar_personagem()
        elif escolha == '2':
            iniciar_jogo()
        elif escolha == '3':
            print("\nObrigado por jogar! Até a próxima.")
            break
        else:
            print("\nOpção inválida. Tente novamente.")
            time.sleep(2)

if __name__ == "__main__":
    # Garante que o Docker está rodando antes de começar
    conn_test = get_all_characters()
    if conn_test is not None:
        main_menu()