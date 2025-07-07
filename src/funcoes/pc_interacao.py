from database import get_sala_id, get_pcs_in_room
from .inimigos import verificar_e_gerar_inimigos, contar_inimigos_no_pc, pc_esta_inutilizavel
from .batalha import get_inimigos_no_pc

def acessar_pc_menu(personagem_id):
    sala_id = get_sala_id(personagem_id)
    pcs = get_pcs_in_room(sala_id)
    if not pcs:
        print("Não há computadores nesta sala.")
        return

    print("\nComputadores disponíveis nesta sala:")
    for i, (id_pc, tipo) in enumerate(pcs, start=1):
        num_inimigos = contar_inimigos_no_pc(id_pc)
        if tipo == 'Bugado':
            status = " (PC Bugado)"
        elif pc_esta_inutilizavel(id_pc):
            status = f" (INUTILIZÁVEL - {num_inimigos} inimigos)"
        elif num_inimigos > 0:
            status = f" ({num_inimigos} inimigos)"
        else:
            status = " (Limpo)"
        print(f"  [{i}] PC #{id_pc}{status}")
    print("  [0] Cancelar")

    escolha = int(input("Escolha um PC para acessar: ").strip())
    if escolha == 0:
        return
    if 1 <= escolha <= len(pcs):
        id_pc_escolhido = pcs[escolha - 1][0]
        print(f"\nVocê acessou o PC #{id_pc_escolhido}.")
        acessar_pc(id_pc_escolhido, personagem_id)
    else:
        print("Opção inválida.")

def acessar_pc(id_pc, personagem_id):
    # Verifica se precisa gerar inimigo automaticamente
    verificar_e_gerar_inimigos()
    print(f"Você acessou o PC #{id_pc}.")
    inimigos = get_inimigos_no_pc(id_pc)
    if inimigos and personagem_id is not None:
        print("Você foi atacado por inimigos! Entrando em modo batalha...")
        from .batalha import batalha_interface
        batalha_interface(id_pc, personagem_id)