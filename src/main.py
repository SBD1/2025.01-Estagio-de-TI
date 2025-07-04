import os
import time
import unicodedata
from database import call_db_function, get_all_characters, get_location_details

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto.lower().strip()) if unicodedata.category(c) != 'Mn')

def criar_personagem():
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

def game_loop(personagem_id, personagem_nome):
    clear_screen()
    print(f"Iniciando o jogo com {personagem_nome}...")
    time.sleep(2)

    while True:
        clear_screen()
        location_details = get_location_details(personagem_id)

        if not location_details:
            print("Erro ao carregar o local. Voltando ao menu.")
            time.sleep(3)
            break

        nome_sala, descricao_sala, saidas_disponiveis = location_details
        print(f"--- {personagem_nome} ---")
        print(f"Você está no: {nome_sala}")
        print(descricao_sala)
        print("\n--------------------")
        print("O que você faz?\n")

        saidas_disponiveis = saidas_disponiveis or []
        for i, saida in enumerate(saidas_disponiveis, start=1):
            print(f"  [{i}] {saida}")

        opc_falar = False
        if "deposito" in normalizar(nome_sala):
            print(f"  [{len(saidas_disponiveis) + 1}] Falar com Almoxarife")
            opc_falar = True
        print(f"  [{len(saidas_disponiveis) + 2 if opc_falar else len(saidas_disponiveis) + 1}] Voltar ao menu principal")
        print("\n--------------------")

        try:
            escolha_str = input("Sua escolha: ").strip()
            if not escolha_str:
                continue

            escolha_num = int(escolha_str)

            if opc_falar and escolha_num == len(saidas_disponiveis) + 1:
                print("\n[ALMOXARIFE] Bem-vindo! Estes são os itens disponíveis:")
                resposta = call_db_function('listar_itens_almoxarifado')
                if isinstance(resposta, list):
                    for item in resposta:
                        print(f" - {item[1]} ({item[3]} moedas): {item[2]}")
                    id_item = input("\nDigite o ID do item que deseja comprar (ou Enter para sair): ").strip()
                    if id_item:
                        retorno = call_db_function('comprar_item', personagem_id, int(id_item))
                        print(retorno)
                        time.sleep(3)
                else:
                    print("Erro ao listar itens.")
                    time.sleep(2)

            elif escolha_num == (len(saidas_disponiveis) + 2 if opc_falar else len(saidas_disponiveis) + 1):
                print("\nVoltando ao menu principal...")
                time.sleep(2)
                break

            elif 1 <= escolha_num <= len(saidas_disponiveis):
                direcao_escolhida = saidas_disponiveis[escolha_num - 1]
                print(f"\nTentando: {direcao_escolhida}...")
                call_db_function('mover_personagem', personagem_id, direcao_escolhida)
                time.sleep(1)

            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(2)

        except ValueError:
            print("\nPor favor, digite um número. Tente novamente.")
            time.sleep(2)

def main_menu():
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
