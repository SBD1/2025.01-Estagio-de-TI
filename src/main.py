import os
import time
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
        personagem_selecionado = next((p for p in personagens if p[0] == escolha), None)

        if not personagem_selecionado:
            raise ValueError

        game_loop(personagem_selecionado[0], personagem_selecionado[1])

    except (ValueError, IndexError):
        print("\nOpção inválida. Retornando ao menu principal.")
        time.sleep(2)

def abrir_loja(personagem_id, item_type):
    """Interface simples de compra de itens."""
    while True:
        clear_screen()
        itens = get_items_for_sale(item_type)
        coins = get_player_coins(personagem_id)
        nome_loja = 'Loja'
        if item_type == 'Consumivel':
            nome_loja = 'Cafeteria'
        elif item_type == 'Equipamento':
            nome_loja = 'Depósito'
        print(f"=== {nome_loja} ===  (Coins: {coins} C$)\n")
        if not itens:
            print("A loja está vazia.")
            input("Pressione Enter para voltar.")
            return

        for i, (inst_id, nome, desc, preco, qtd, bonus_atk, bonus_def, bonus_hp) in enumerate(itens, start=1):
            print(f"[{i}] {nome} - {preco} C$ (x{qtd})")
            atributos = []
            if bonus_hp:
                atributos.append(f"Vida +{bonus_hp}")
            if bonus_atk:
                atributos.append(f"Ataque +{bonus_atk}")
            if bonus_def:
                atributos.append(f"Defesa +{bonus_def}")
            attr_text = f" [{', '.join(atributos)}]" if atributos else ""
            print(f"    {desc}{attr_text}")
        print("[0] Voltar")

        escolha = input("Escolha um item: ").strip()
        if escolha == "0":
            return
        try:
            idx = int(escolha)
            if 1 <= idx <= len(itens):
                inst_id = itens[idx - 1][0]
                max_q = itens[idx - 1][4]
                q = input(f"Quantidade (1-{max_q}): ").strip()
                q = int(q) if q else 1
                if q < 1 or q > max_q:
                    print("Quantidade inválida.")
                    time.sleep(2)
                    continue
                msg = buy_item(personagem_id, inst_id, q)
                print(msg)
                time.sleep(2)
            else:
                print("Opção inválida.")
                time.sleep(2)
        except ValueError:
            print("Digite números válidos.")
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

# DEFINIÇÃO DO MENU DO ELEVADOR (AGORA POSICIONADA ANTES DE SER CHAMADA)
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

# GAME LOOP QUE CHAMA A FUNÇÃO 'menu_elevador'
def game_loop(personagem_id, personagem_nome):
    """O loop principal do jogo, com menu de opções numérico."""
    clear_screen()
    print(f"Iniciando o jogo com {personagem_nome}...")
    print("(Pressione 'p' a qualquer momento para ver seu status)" )
    time.sleep(2)

    while True:
        clear_screen()

        location_details = get_location_details(personagem_id)
        sala_info = get_player_room_info(personagem_id)

        if not location_details:
            print("Erro ao carregar o local. Voltando ao menu.")
            time.sleep(3)
            break

        nome_sala, descricao_sala, saidas_disponiveis = location_details
        sala_id = sala_info[0] if sala_info else None
        
        saidas_disponiveis = saidas_disponiveis or []

        # Verifica se a opção do elevador está disponível
        elevador_disponivel = "Chamar Elevador" in saidas_disponiveis
        
        npcs_na_sala = get_npcs_in_room(sala_id) if sala_id else []
        tem_vendedor = any(tipo in ('almoxarife', 'barista') for _, _, tipo in npcs_na_sala)

        loja_tipo = None
        if sala_info:
            nome_atual = sala_info[1]
            if nome_atual == 'Cafeteria':
                loja_tipo = 'Consumivel'
            elif nome_atual == 'Depósito':
                loja_tipo = 'Equipamento'

        loja_disponivel = tem_vendedor and loja_tipo is not None

        print(f"--- {personagem_nome} ---")
        print(f"Você está em: {nome_sala}")
        print(descricao_sala)
        print("\n--------------------")
        print("O que você faz?\n")

        opcoes_menu = [s for s in saidas_disponiveis]
        
        for i, saida in enumerate(opcoes_menu, start=1):
            print(f"  [{i}] {saida}")

        next_idx = len(opcoes_menu) + 1
        if loja_disponivel:
            print(f"  [{next_idx}] Comprar Itens")
            next_idx += 1

        print("  [P] Ver status do personagem")
        print(f"  [{next_idx}] Voltar ao menu principal")
        print("\n--------------------")

        try:
            escolha_str = input("Sua escolha: ").strip()
            if not escolha_str:
                continue
            if escolha_str.lower() == 'p':
                mostrar_status(personagem_id)
                continue

            escolha_num = int(escolha_str)
            
            if 1 <= escolha_num <= len(opcoes_menu):
                opcao_escolhida = opcoes_menu[escolha_num - 1]

                if opcao_escolhida == "Chamar Elevador":
                    # A chamada agora funciona porque menu_elevador está definido acima
                    menu_elevador(personagem_id)
                else: 
                    print(f"\nTentando: {opcao_escolhida}...")
                    call_db_function('mover_personagem', personagem_id, opcao_escolhida)
                    time.sleep(1)
            else:
                loja_idx = len(opcoes_menu) + 1 if loja_disponivel else -1
                sair_idx = len(opcoes_menu) + 2 if loja_disponivel else len(opcoes_menu) + 1

                if loja_disponivel and escolha_num == loja_idx:
                    abrir_loja(personagem_id, loja_tipo)
                elif escolha_num == sair_idx:
                    print("\nVoltando ao menu principal...")
                    time.sleep(2)
                    break
                else:
                    print("\nOpção inválida. Tente novamente.")
                    time.sleep(2)
        except (ValueError):
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
    conn_test = get_all_characters()
    if conn_test is not None:
        main_menu()