from .gerencia_inventario import consumir_item, usar_powerup, dropar_item

def get_inventario_itens(personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                i.nome,
                ii.quantidade,
                i.tipo,
                i.recuperacao_vida,
                i.bonus_ataque,
                ii.id_instancia
            FROM Inventario inv
            JOIN ItemInventario ii ON inv.id_inventario = ii.id_inventario
            JOIN InstanciaItem inst ON ii.id_instancia = inst.id_instancia
            JOIN Item i ON inst.id_item = i.id_item
            WHERE inv.id_estagiario = %s;
        """, (personagem_id,))
        itens = cur.fetchall()
    conn.close()
    return itens

from database import get_connection

def get_detalhes_item(id_instancia):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT i.descricao, i.preco_base, i.dano
            FROM InstanciaItem inst
            JOIN Item i ON inst.id_item = i.id_item
            WHERE inst.id_instancia = %s;
        """, (id_instancia,))
        resultado = cur.fetchone()
    conn.close()
    return resultado


def abrir_inventario(personagem_id):
    itens = get_inventario_itens(personagem_id)
    if not itens:
        print("\nSeu inventário está vazio.")
        input("\nPressione Enter para voltar...")
        return

    while True:
        print("\n--- Seu Inventário ---")
        for idx, (nome_item, quantidade, tipo, _, _, id_instancia) in enumerate(itens, 1):
            print(f"  [{idx}] {nome_item} x{quantidade} ({tipo})")
        print("  [0] Voltar")

        escolha_str = input("\nEscolha um item ou [0] para voltar: ").strip()
        if not escolha_str.isdigit():
            print("Opção inválida.")
            continue

        escolha = int(escolha_str)
        if escolha == 0:
            break
        if escolha < 1 or escolha > len(itens):
            print("Opção inválida.")
            continue

        item = itens[escolha - 1]
        nome, qtd, tipo, rec_vida, bonus, id_instancia = item

        while True:
            print(f"\nVocê selecionou: {nome} ({tipo})")
            print("  [1] Ver detalhes")
            if tipo == 'Consumivel':
                print("  [2] Consumir")
                print("  [3] Dropar")
            elif tipo == 'PowerUp':
                print("  [2] Usar")
                print("  [3] Dropar")
            else:  # Arma ou outro
                print("  [2] Ler")
                print("  [3] Dropar")
            print("  [0] Voltar")

            acao = input("Escolha uma ação: ").strip()

            if acao == '0':
                break
            elif acao == '1':
                detalhes = get_detalhes_item(id_instancia)
                if detalhes:
                    descricao, valor, dano = detalhes
                    print("\n--- Detalhes ---")
                    print(f"Descrição: {descricao}")
                    print(f"Valor: {valor} coins")
                    if tipo == 'Arma':
                        print(f"Dano: {dano}")
                    elif tipo == 'Consumivel':
                        print(f"Recupera: {rec_vida} HP")
                    elif tipo == 'PowerUp':
                        print(f"Bônus de ataque: {bonus}")
                else:
                    print("Detalhes indisponíveis.")
            elif acao == '2':
                if tipo == 'Consumivel':
                    consumir_item(personagem_id, id_instancia, rec_vida, nome)
                    break
                elif tipo == 'PowerUp':
                    usar_powerup(personagem_id, id_instancia, bonus, nome)
                    break
                elif tipo == 'Arma':
                    conn = get_connection()
                    with conn.cursor() as cur:
                        # Verifica se já foi lido
                        cur.execute("""
                            SELECT lido FROM InstanciaItem WHERE id_instancia = %s
                        """, (id_instancia,))
                        lido = cur.fetchone()[0]
                        if lido:
                            print(f"\nVocê já leu o livro \"{nome}\".")
                        else:
                            # Marca como lido
                            cur.execute("""
                                UPDATE InstanciaItem SET lido = TRUE WHERE id_instancia = %s
                            """, (id_instancia,))
                            conn.commit()
                            print(f"\nVocê leu o livro \"{nome}\" com atenção...")
                            # Aqui o trigger do banco insere os ataques automaticamente
                    conn.close()
                    break
            elif acao == '3' and tipo in ('Consumivel', 'PowerUp', 'Arma'):
                dropar_item(id_instancia, nome)
                break
            else:
                print("Ação inválida.")

        input("\nPressione Enter para continuar...")
        itens = get_inventario_itens(personagem_id)  # Atualiza inventário
