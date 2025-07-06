import os
import time
from database import call_db_function, get_all_characters
from database import call_db_function, get_all_characters, get_location_details
from funcoes.inimigos import *
from funcoes.navegacao import *
from funcoes.pc_interacao import *
from funcoes.personagem import *


def clear_screen():
    #Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_personagem():

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
    #Lida com a seleção de personagem e o início do loop do jogo
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
        clear_screen()
        print(f"Iniciando o jogo com {personagem_selecionado[1]}...")
        time.sleep(2)
        game_loop(personagem_selecionado[0], personagem_selecionado[1])

    except (ValueError, IndexError):
        print("\nOpção inválida. Retornando ao menu principal.")
        time.sleep(2)

def game_loop(personagem_id, personagem_nome):
    # Verifica se precisa gerar inimigos automaticamente no início
    verificar_e_gerar_inimigos()

    while True:
        clear_screen()
        if not exibir_local(personagem_id, personagem_nome):
            break
        opcoes, saidas = montar_opcoes(personagem_id)
        exibir_opcoes(opcoes)
        if not processar_escolha(personagem_id, opcoes, saidas):
            break
    
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