from database import call_db_function, get_connection

from database import get_connection

from .inimigos import listar_pcs_com_problemas



def falar_com_npc(id_npc, npc_nome, npc_tipo, id_estagiario):
    pode = call_db_function('pode_conversar_com_npc', id_estagiario, id_npc)
    if not pode:
        print("Nem olha na minha cara novato!")
    if npc_tipo == 'recepcionista':

        print("\n--- RECEPCIONISTA ---")
        print("Recepcionista: Olá estagiário, outros funcionários relataram um problema para você resolver.")

        pcs_com_problemas = listar_pcs_com_problemas()

        if pcs_com_problemas:
            print(f"Recepcionista: Os seguintes PCs estão com problemas: {', '.join(f'PC #{pc}' for pc in pcs_com_problemas)}")
        else:
            print("Recepcionista: No momento, todos os PCs estão funcionando normalmente!")

        print("Recepcionista: Boa sorte com os reparos!")
        print("--------------------")


    if npc_tipo == 'colega':

        print("\n--- COLEGA ---")
        print("Colega: Oi! Como vai o trabalho?")
        print("\nOpções:")
        print("  [1] Perguntar sobre o trabalho")
        print("  [2] Pedir ajuda")
        print("  [3] Sair")

        escolha = input("\nSua escolha: ").strip()

        if escolha == '1':
            print("Colega: Está tudo corrido por aqui. Os computadores vivem dando problema!")
        elif escolha == '2':
            print("Colega: Infelizmente não posso ajudar muito, mas boa sorte!")
        elif escolha == '3':
            print("Colega: Até mais!")
        else:
            print("Colega: Não entendi...")


    elif npc_tipo == 'chefe':

        print("\n--- CHEFE ---")
        print("Chefe: Estagiário! Como anda o trabalho?")
        print("\nOpções:")
        print("  [1] Relatório de progresso")
        print("  [2] Pedir orientação")
        print("  [3] Sair")

        escolha = input("\nSua escolha: ").strip()

        if escolha == '1':
            print("Chefe: Ótimo! Continue assim. A empresa precisa de pessoas dedicadas.")
        elif escolha == '2':
            print("Chefe: Foque nos PCs com problemas. É prioridade máxima!")
        elif escolha == '3':
            print("Chefe: Volte ao trabalho!")
        else:
            print("Chefe: Concentre-se no que eu disse!")

        
    elif npc_tipo == 'almoxarife':
        
        print("\n--- ALMOXARIFE ---")
        print("Almoxarife: Precisa de algum equipamento?")
        print("\nOpções:")
        print("  [1] Ver equipamentos disponíveis")
        print("  [2] Pedir ferramenta")
        print("  [3] Sair")

        escolha = input("\nSua escolha: ").strip()

        if escolha == '1':
            print("Almoxarife: Temos cabos, teclados, mouses... o básico para manutenção.")
        elif escolha == '2':
            print("Almoxarife: Pegue o que precisar, mas devolva depois!")
        elif escolha == '3':
            print("Almoxarife: Até logo!")
        else:
            print("Almoxarife: Não temos isso aqui...")

    elif npc_tipo == 'supervisor':
        
        print("\n--- SUPERVISOR ---")
        print("Almoxarife: Quer alguma missão?")
        print("\nOpções:")
        print("  [1] Aceitar")
        print("  [2] Sair")

        escolha = input("\nSua escolha: ").strip()

        if escolha == '1':
            print("Supervisor: Que bom que você aceitou.")
        elif escolha == '2':
            print("Supervisor: Uma hora ou outra você vai ter que passar por mim.")

        else:
            print("Me responde primeiro!")

    input("\nPressione Enter para continuar...")
