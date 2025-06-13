import os
import time
from database import call_db_function, get_all_characters

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

def game_loop(personagem_id, personagem_nome):
    """O loop principal do jogo, onde o jogador interage com o mundo."""
    clear_screen()
    print(f"Iniciando o jogo com {personagem_nome}...")
    time.sleep(2)

    # Pega a descrição inicial do local do personagem
    descricao_local = call_db_function('descrever_local_atual', personagem_id)

    while True:
        clear_screen()
        print(f"--- {personagem_nome} ---")
        print(descricao_local)
        print("\n--------------------")
        
        # O comando do jogador é a direção para onde ele quer ir
        comando = input("\nO que você faz? (digite uma saída ou 'sair' para voltar ao menu)\n> ").strip().lower()

        if comando == 'sair':
            print("\nVoltando ao menu principal...")
            time.sleep(2)
            break
        elif not comando:
            continue
        
        # Chama a função SQL para mover o personagem
        # O banco de dados retorna a nova descrição ou uma mensagem de erro
        resultado_movimento = call_db_function('mover_personagem', personagem_id, comando)
        descricao_local = resultado_movimento


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