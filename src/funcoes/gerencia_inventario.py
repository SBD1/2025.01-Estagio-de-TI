# inventario_acoes.py
from database import get_connection, get_sala_id, get_itens_no_chao

def dropar_item(id_instancia, nome_item):
    from database import get_sala_id
    # Descobre em qual sala está o personagem dono do item
    conn = get_connection()
    with conn.cursor() as cur:
        # Descobre o personagem dono do item
        cur.execute("""
            SELECT id_estagiario FROM InstanciaItem WHERE id_instancia = %s
        """, (id_instancia,))
        row = cur.fetchone()
        personagem_id = row[0]
        cur.execute("""
            SELECT sala_atual FROM Estagiario WHERE id_personagem = %s
        """, (personagem_id,))
        row = cur.fetchone()
        sala_id = row[0]

        # Atualiza a instância para estar no chão na sala correta
        cur.execute("""
            UPDATE InstanciaItem
            SET local_atual = 'Chao', id_sala = %s, id_estagiario = NULL
            WHERE id_instancia = %s
        """, (sala_id, id_instancia))

        # Remove a ligação com o inventário
        cur.execute("""
            DELETE FROM ItemInventario
            WHERE id_instancia = %s
        """, (id_instancia,))

        conn.commit()
    conn.close()
    print(f"Você dropou o item: {nome_item}")

def consumir_item(personagem_id, id_instancia, rec_vida, nome_item):
    # Exemplo: atualizar vida do personagem
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Estagiario
            SET respeito = LEAST(respeito + %s, 100)
            WHERE id_personagem = %s
        """, (rec_vida, personagem_id))

        # Remove do inventário e instancia
        cur.execute("DELETE FROM ItemInventario WHERE id_instancia = %s", (id_instancia,))
        cur.execute("DELETE FROM InstanciaItem WHERE id_instancia = %s", (id_instancia,))

        conn.commit()
    conn.close()
    print(f"Você consumiu: {nome_item} e recuperou {rec_vida} de respeito!")

def usar_powerup(personagem_id, id_instancia, bonus, nome_item):
    # Exemplo: aumentar respeito temporariamente
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Estagiario
            SET respeito = LEAST(respeito + %s, 100)
            WHERE id_personagem = %s
        """, (bonus, personagem_id))

        # Remove do inventário e instancia
        cur.execute("DELETE FROM ItemInventario WHERE id_instancia = %s", (id_instancia,))
        cur.execute("DELETE FROM InstanciaItem WHERE id_instancia = %s", (id_instancia,))

        conn.commit()
    conn.close()
    print(f"Você usou o PowerUp: {nome_item} e ganhou {bonus} de respeito!")

def pegar_item_do_chao(personagem_id):
    sala_id = get_sala_id(personagem_id)
    itens = get_itens_no_chao(sala_id)

    print("\n--- Itens no chão ---")
    for idx, (_, nome) in enumerate(itens, 1):
        print(f"  [{idx}] {nome}")
    print("  [0] Cancelar")

    escolha = input("Escolha um item para pegar: ").strip()
    if not escolha.isdigit():
        print("Escolha inválida.")
        return
    escolha = int(escolha)
    if escolha == 0 or escolha > len(itens):
        return

    id_instancia_escolhida = itens[escolha - 1][0]

    # Atualiza local do item para Inventario
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id_inventario FROM Inventario WHERE id_estagiario = %s;
        """, (personagem_id,))
        id_inventario = cur.fetchone()[0]

        cur.execute("""
        UPDATE InstanciaItem
        SET local_atual = 'Inventario', id_estagiario = %s, id_sala = NULL
        WHERE id_instancia = %s;
    """, (personagem_id, id_instancia_escolhida))

        conn.commit()
    conn.close()

    print("Item adicionado ao inventário!")
