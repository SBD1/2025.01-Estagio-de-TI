from database import get_connection, call_db_function
import random

def get_ataques_personagem(personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.id_ataque, a.nome, a.dano, a.chance_acerto
            FROM Ataque a
            JOIN PersonagemAtaque pa ON pa.id_ataque = a.id_ataque
            WHERE pa.personagem_id = %s
        """, (personagem_id,))
        ataques = cur.fetchall()
    conn.close()
    return ataques

def get_inimigos_no_pc(id_pc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT ii.id_instancia, i.nome, ii.vida
            FROM InstanciaInimigo ii
            JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
            WHERE ii.id_pc = %s
        """, (id_pc,))
        inimigos = cur.fetchall()
    conn.close()
    return inimigos

def atacar_inimigo(id_ataque, id_inimigo_instancia):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT dano FROM Ataque WHERE id_ataque = %s", (id_ataque,))
        dano = cur.fetchone()[0]
        cur.execute("UPDATE InstanciaInimigo SET vida = GREATEST(vida - %s, 0) WHERE id_instancia = %s", (dano, id_inimigo_instancia))
        conn.commit()
    conn.close()

def remover_inimigos_mortos(id_pc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM InstanciaInimigo WHERE id_pc = %s AND vida <= 0", (id_pc,))
        conn.commit()
    conn.close()

def batalha_interface(id_pc, personagem_id):
    while True:
        inimigos = get_inimigos_no_pc(id_pc)
        if not inimigos:
            print("Todos os inimigos foram derrotados! Parabéns!")
            break

        print("\n--- BATALHA ---")
        print("Inimigos no PC:")
        for idx, (id_instancia, nome, vida) in enumerate(inimigos, 1):
            print(f"  [{idx}] {nome} (HP: {vida})")

        ataques = get_ataques_personagem(personagem_id)
        print("\nSeus ataques:")
        for idx, (id_ataque, nome, dano, chance) in enumerate(ataques, 1):
            print(f"  [{idx}] {nome} (Dano: {dano}, Chance: {chance}%)")
        print("  [0] Fugir")

        escolha_ataque = input("Escolha seu ataque: ").strip()
        if escolha_ataque == "0":
            print("Você fugiu da batalha!")
            break
        if not escolha_ataque.isdigit() or not (1 <= int(escolha_ataque) <= len(ataques)):
            print("Opção inválida.")
            continue

        ataque_escolhido = ataques[int(escolha_ataque) - 1]
        id_ataque = ataque_escolhido[0]

        escolha_alvo = input("Escolha o inimigo para atacar: ").strip()
        if not escolha_alvo.isdigit() or not (1 <= int(escolha_alvo) <= len(inimigos)):
            print("Alvo inválido.")
            continue

        id_inimigo_instancia = inimigos[int(escolha_alvo) - 1][0]


        if random.randint(1, 100) <= ataque_escolhido[3]:
            atacar_inimigo(id_ataque, id_inimigo_instancia)
            print("Ataque acertou!")
        else:
            print("Você errou o ataque!")

        remover_inimigos_mortos(id_pc)
        # Aqui você pode implementar o turno dos inimigos atacando o jogador, se quiser