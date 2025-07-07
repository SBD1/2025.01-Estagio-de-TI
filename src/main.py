import os
import time
import sys
# >> IMPORTS ATUALIZADOS <<
from database import (
    call_db_function,
    get_all_characters,
    get_location_details,
    get_player_room_info,
    get_npcs_in_room,
    get_items_for_sale,
    get_player_coins,
    get_player_stats,
    buy_item,
    use_elevator,
    get_all_floors,
    get_interactable_mission_in_room,
    get_inimigos_na_sala,
    get_player_inventory # Adicionado para o inventário
)
import interacoes


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

    mensagem = call_db_function('criar_personagem', nome)
    print(f"\n{mensagem}")
    time.sleep(3)

def exibir_introducao(nome_personagem):
    """Exibe o texto de introdução do jogo com efeito de digitação."""
    clear_screen()
    
    texto_intro = f"""
    Bem-vindo, {nome_personagem}, um jovem estagiário de TI cheio de sonhos.
    Seu objetivo? Ser contratado como Desenvolvedor Júnior numa das maiores
    empresas de tecnologia da cidade.

    Mas para isso, você precisa provar seu valor — começando pelo básico
    (como instalar impressoras e arrumar cabos) até tarefas cada vez mais
    desafiadoras (programar sistemas, integrar APIs, criar bancos de dados).

    Cada andar do prédio representa uma etapa da sua evolução dentro da empresa!

    --- ESTRUTURA DO JOGO ---

    Neste RPG, você é um estagiário de TI em busca da tão sonhada efetivação.
    Cada andar de um prédio corporativo representa um novo desafio técnico e
    profissional. Supere todos os andares para alcançar o topo e conquistar
    seu cargo!

    - Subsolo 2 (Servidor): Onde está alocado o servidor da empresa. Cuidado com o frio!
    - Subsolo 1 (Almoxarifado): Itens de suporte (peças, cabos, drivers, ferramentas).
    - Térreo (Recepção/Cafeteria): Base para missões e compra de consumíveis.
    - Andares 1 a 10: Cada andar é um setor da empresa com desafios diferentes.

    """
    
    for caractere in texto_intro:
        print(caractere, end='', flush=True)
        if caractere in ['.', '!', '?']:
            time.sleep(0.5)
        elif caractere in [',', ';', ':']:
            time.sleep(0.25)
        else:
            time.sleep(0.03)

    input("\nPressione Enter para começar sua jornada...")

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
        personagem_selecionado = next((p for p in personagens if p[0] == escolha), None)

        if not personagem_selecionado:
            raise ValueError
        
        exibir_introducao(personagem_selecionado[1])
        game_loop(personagem_selecionado[0], personagem_selecionado[1])

    except (ValueError, IndexError):
        print("\nOpção inválida. Retornando ao menu principal.")
        time.sleep(2)

def abrir_loja(personagem_id, loja_info):
    """
    Interface de compra de itens.
    'loja_info' é uma tupla (nome_da_loja, tipo_de_item).
    """
    nome_loja, item_type = loja_info
    
    while True:
        clear_screen()
        itens = get_items_for_sale(item_type)
        coins = get_player_coins(personagem_id)

        print(f"=== BEM-VINDO À {nome_loja.upper()} ===")
        print(f"Você tem: {coins} C$\n")

        if not itens:
            print("Não há nada para vender aqui no momento.")
            input("\nPressione Enter para voltar.")
            return

        print("Itens disponíveis:\n")
        for i, (inst_id, nome, desc, preco, qtd, bonus_atk, bonus_def, bonus_hp) in enumerate(itens, start=1):
            print(f" [{i}] {nome} - {preco} C$ (Disponível: {qtd})")
            
            atributos = []
            if bonus_hp > 0: atributos.append(f"Vida +{bonus_hp}")
            if bonus_atk > 0: atributos.append(f"Ataque +{bonus_atk}")
            if bonus_def > 0: atributos.append(f"Defesa +{bonus_def}")
            attr_text = f" [{', '.join(atributos)}]" if atributos else ""
            
            print(f"     ↳ {desc}{attr_text}\n")
            
        print(" [0] Voltar")
        print("\n--------------------")

        try:
            escolha_str = input("O que deseja comprar? ").strip()
            if not escolha_str or escolha_str == "0":
                return
            
            idx = int(escolha_str)
            if 1 <= idx <= len(itens):
                inst_id, _, _, _, max_q, _, _, _ = itens[idx - 1]
                
                qnt_str = input(f"Quantidade (1-{max_q}, Enter para 1): ").strip()
                quantidade = int(qnt_str) if qnt_str.isdigit() and int(qnt_str) > 0 else 1

                if 1 <= quantidade <= max_q:
                    mensagem = buy_item(personagem_id, inst_id, quantidade)
                    print(f"\n{mensagem}")
                    time.sleep(2)
                else:
                    print("\nQuantidade inválida.")
                    time.sleep(2)
            else:
                print("\nOpção inválida.")
                time.sleep(2)
        except ValueError:
            print("\nPor favor, digite um número válido.")
            time.sleep(2)

def mostrar_status(personagem_id):
    """Exibe os atributos atuais do personagem."""
    clear_screen()
    stats = get_player_stats(personagem_id)
    if not stats:
        print("Não foi possível obter os dados do personagem.")
        input("Pressione Enter para continuar...")
        return
    nome, nivel, xp, respeito, coins, ataque, defesa, vida, status = stats
    print("=== STATUS DO PERSONAGEM ===\n")
    print(f"Nome: {nome}")
    print(f"Nível: {nivel}")
    print(f"XP: {xp}")
    print(f"Respeito: {respeito}")
    print(f"Coins: {coins} C$")
    print(f"Ataque: {ataque}")
    print(f"Defesa: {defesa}")
    print(f"Vida: {vida}")
    print(f"Status: {status}")
    print("\n===========================")
    input("Pressione Enter para continuar...")

def menu_elevador(personagem_id):
    """Exibe o menu de seleção de andares para o elevador."""
    clear_screen()
    print("--- PAINEL DO ELEVADOR ---\n")
    andares = get_all_floors()
    if not andares:
        print("Erro ao carregar os andares.")
        time.sleep(2)
        return

    for i, (numero, nome) in enumerate(andares, start=1):
        nome_andar = nome.split(": ", 1)[-1]
        print(f"  [{i}] {numero}º Andar - {nome_andar}")

    print("\n  [0] Sair do elevador")
    print("\n--------------------")

    try:
        escolha = int(input("Digite o número do andar de destino: ").strip())
        if escolha == 0:
            return
        if 1 <= escolha <= len(andares):
            andar_destino = andares[escolha - 1][0]
            mensagem = use_elevator(personagem_id, andar_destino)
            print(f"\n{mensagem}")
            time.sleep(2)
        else:
            print("\nAndar inválido.")
            time.sleep(2)
    except (ValueError):
        print("\nPor favor, digite um número válido.")
        time.sleep(2)

def game_loop(personagem_id, personagem_nome):
    """O loop principal do jogo, com menu de opções dinâmico."""
    while True:
        clear_screen()

        location_details = get_location_details(personagem_id)
        sala_info = get_player_room_info(personagem_id)

        if not location_details or not sala_info:
            print("Erro ao carregar o local. Voltando ao menu.")
            time.sleep(3)
            break

        nome_sala, descricao_sala, saidas_disponiveis = location_details
        sala_id, nome_sala_atual, _ = sala_info
        
        saidas_disponiveis = saidas_disponiveis or []
        npcs_na_sala = get_npcs_in_room(sala_id)
        interactable_mission = get_interactable_mission_in_room(personagem_id, sala_id)
        inimigos_na_sala = get_inimigos_na_sala(sala_id)

        loja_info = None
        if npcs_na_sala:
            tem_barista = any(npc[2] == 'barista' for npc in npcs_na_sala)
            tem_almoxarife = any(npc[2] == 'almoxarife' for npc in npcs_na_sala)
            
            if nome_sala_atual == 'Cafeteria' and tem_barista:
                loja_info = ('Cafeteria', 'Consumivel')
            elif nome_sala_atual == 'Depósito' and tem_almoxarife:
                loja_info = ('Almoxarifado', 'Equipamento')

        print(f"--- {personagem_nome} ---")
        print(f"Você está em: {nome_sala}")
        print(descricao_sala)
        
        if npcs_na_sala:
            print("\nVocê vê por aqui:")
            for _, nome_npc, tipo_npc in npcs_na_sala:
                print(f"- {nome_npc} ({tipo_npc})")
        
        if inimigos_na_sala:
            print("\n\033[91mPERIGO! Há inimigos nesta sala!\033[0m")

        print("\n--------------------")
        print("O que você faz?\n")

        # Constrói o menu dinamicamente
        opcoes_menu = {i + 1: saida for i, saida in enumerate(saidas_disponiveis)}
        next_idx = len(opcoes_menu) + 1

        loja_idx, combat_idx, talk_idx, interact_idx, tasks_idx, inventory_idx = -1, -1, -1, -1, -1, -1

        if loja_info:
            opcoes_menu[next_idx] = f"Comprar na {loja_info[0]}"
            loja_idx = next_idx
            next_idx += 1
        
        if inimigos_na_sala:
            opcoes_menu[next_idx] = "Entrar em Combate"
            combat_idx = next_idx
            next_idx += 1

        if npcs_na_sala:
            opcoes_menu[next_idx] = "Falar com alguém"
            talk_idx = next_idx
            next_idx += 1

        if interactable_mission:
            opcoes_menu[next_idx] = "Interagir com o ambiente"
            interact_idx = next_idx
            next_idx += 1
            
        opcoes_menu[next_idx] = "Ver Tarefas (Missões)"
        tasks_idx = next_idx
        next_idx += 1
        
        # Adiciona a opção de inventário ao menu
        opcoes_menu[next_idx] = "Ver Inventário"
        inventory_idx = next_idx
        
        # Exibe o menu
        for idx, desc in sorted(opcoes_menu.items()):
            print(f"  [{idx}] {desc}")
        print("\n  [P] Ver status do personagem")
        print("  [0] Voltar ao menu principal")
        print("\n--------------------")

        try:
            escolha_str = input("Sua escolha: ").strip().lower()
            if not escolha_str:
                continue
            
            if escolha_str == 'p':
                mostrar_status(personagem_id)
                continue
            
            # Adiciona a opção de inventário ao tratamento de input
            if escolha_str == 'i': # Atalho para inventário
                clear_screen()
                interacoes.exibir_inventario(personagem_id)
                continue

            escolha_num = int(escolha_str)

            if escolha_num == 0:
                print("\nVoltando ao menu principal...")
                time.sleep(2)
                break

            if escolha_num in opcoes_menu:
                opcao_escolhida = opcoes_menu[escolha_num]
                
                if opcao_escolhida in saidas_disponiveis:
                    if "Elevador" in opcao_escolhida:
                        menu_elevador(personagem_id)
                    else:
                        call_db_function('mover_personagem', personagem_id, opcao_escolhida)
                    time.sleep(1)
                elif escolha_num == loja_idx:
                    abrir_loja(personagem_id, loja_info)
                elif escolha_num == combat_idx:
                    interacoes.iniciar_combate(personagem_id, sala_id)
                elif escolha_num == talk_idx:
                    interacoes.conversar_com_npc(personagem_id, sala_id)
                elif escolha_num == interact_idx:
                    interacoes.interagir_com_ambiente(personagem_id, interactable_mission)
                elif escolha_num == tasks_idx:
                    clear_screen()
                    interacoes.exibir_missoes_e_demandas(personagem_id)
                elif escolha_num == inventory_idx:
                    clear_screen()
                    interacoes.exibir_inventario(personagem_id)
            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(2)

        except ValueError:
            print("\nPor favor, digite um número válido.")
            time.sleep(2)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            time.sleep(3)


def main_menu():
    """Exibe o menu principal e gerencia a navegação."""
    while True:
        clear_screen()
        print("========================================")
        print("      BEM-VINDO À SAGA DO ESTAGIÁRIO    ")
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
    if get_all_characters() is not None:
        main_menu()
