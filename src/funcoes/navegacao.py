from database import get_location_details, get_pcs_in_room, get_sala_id, call_db_function, get_connection, get_itens_no_chao
from .pc_interacao import acessar_pc_menu
from .inimigos import listar_pcs_com_problemas
from .npc_interacao import falar_com_npc
from .abrir_inventario import abrir_inventario
from .gerencia_inventario import pegar_item_do_chao

def exibir_local(personagem_id, personagem_nome):
    location_details = get_location_details(personagem_id)
    if not location_details:
        print("Erro ao carregar o local. Voltando ao menu.")
        return False

    nome_local, descricao, _ = location_details
    sala_id = get_sala_id(personagem_id)
    itens_chao = get_itens_no_chao(sala_id)

    print(f"--- {personagem_nome} ---")
    print(f"Você está no: {nome_local}")
    print(descricao)

    if itens_chao:
        print("\nItens no chão:")
        for item in itens_chao:
            nome_item = item[1]  # Supondo (id_item, nome_item, quantidade)
            qtd = item[2] if len(item) > 2 else 1
            print(f" - {nome_item} (x{qtd})")

    print("\n--------------------")
    print("O que você faz?\n")
    return True


def verificar_npc_na_sala(sala_id):
    # Verifica se há NPCs na sala atual
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT n.id_npc, n.nome, n.tipo
            FROM npc n
            WHERE n.sala_atual = %s;
        """, (sala_id,))
        npcs = cur.fetchall()
    conn.close()
    return npcs

def montar_opcoes(personagem_id):
    # função que mostra todas as opcoes na tela
    location_details = get_location_details(personagem_id)
    saidas_disponiveis = location_details[2] if location_details else []
    sala_id = get_sala_id(personagem_id)
    pcs = get_pcs_in_room(sala_id)
    npcs = verificar_npc_na_sala(sala_id)
    itens_chao = get_itens_no_chao(sala_id)

    #mostra opcoes de salas adjacentes, npc e pc na sala 
    opcoes = []
    for saida in saidas_disponiveis:
        opcoes.append({'tipo': 'saida', 'nome': saida})
    if pcs:
        opcoes.append({'tipo': 'pc', 'nome': 'Acessar PC'})
    if npcs:
        for id_npc, nome_npc, tipo_npc in npcs:
            opcoes.append({'tipo': 'npc', 'id_npc': id_npc, 'nome': f'Falar com {nome_npc}', 'npc_nome': nome_npc, 'npc_tipo': tipo_npc})
    if itens_chao:
        opcoes.append({'tipo': 'pegar_item', 'nome': 'Pegar item do chão'})
    opcoes.append({'tipo': 'inventario', 'nome': 'Abrir Inventário'})
    opcoes.append({'tipo': 'sair', 'nome': 'Voltar ao menu principal'})
    return opcoes, saidas_disponiveis


def exibir_opcoes(opcoes):
    for idx, opcao in enumerate(opcoes, start=1):
        print(f"  [{idx}] {opcao['nome']}")
    print("\n--------------------")

def processar_escolha(personagem_id, opcoes, saidas):
    
    escolha_str = input("Sua escolha: ").strip()
    if not escolha_str:
        return True
    escolha_num = int(escolha_str)

    if not (1 <= escolha_num <= len(opcoes)):
        print("\nOpção inválida. Tente novamente.")
        return True
    opcao = opcoes[escolha_num - 1]

    if opcao['tipo'] == 'saida':
        direcao_escolhida = opcao['nome']
        print(f"\nMovendo para: {direcao_escolhida}...")
        call_db_function('mover_personagem', personagem_id, direcao_escolhida)
        return True

    if opcao['tipo'] == 'pc':
        acessar_pc_menu(personagem_id)
        input("\nPressione Enter para continuar...")
        return True

    if opcao['tipo'] == 'npc':
        falar_com_npc(opcao['id_npc'],opcao['npc_nome'], opcao['npc_tipo'], personagem_id)
        return True
    
    if opcao['tipo'] == 'inventario':
        abrir_inventario(personagem_id)
        return True
    
    if opcao['tipo'] == 'pegar_item':
        pegar_item_do_chao(personagem_id)
        return True

    if opcao['tipo'] == 'sair':
        print("\nVoltando ao menu principal...")
        return False