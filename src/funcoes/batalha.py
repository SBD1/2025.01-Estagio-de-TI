from database import get_connection, call_db_function
import random
from util.limpar_tela import limpar_tela

def get_ataques_personagem(personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.id_ataque, a.nome, a.dano, a.chance_acerto
            FROM Ataque a
            JOIN PersonagemAtaque pa ON pa.id_ataque = a.id_ataque
            WHERE pa.id_personagem = %s
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

def atacar_inimigo(id_arma, id_inimigo_instancia):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT dano FROM Ataque WHERE id_ataque = %s", (id_arma,))
        resultado = cur.fetchone()
        if not resultado:
            print("Ataque não encontrado.")
            return
        dano = resultado[0]
    conn.close()

    id_inimigo = get_id_inimigo_por_instancia(id_inimigo_instancia)
    if not id_inimigo:
        print("Inimigo não encontrado.")
        return
    efeito = get_efeito_contra_inimigo(id_arma, id_inimigo)
    if efeito == 'efetivo':
        print("O ataque foi super efetivo!")
        dano *= 2
    elif efeito == 'inefetivo':
        print("O ataque foi inefetivo!")
        dano = 0
    else:
        print("O ataque teve efeito normal.")

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE InstanciaInimigo
            SET vida = GREATEST(vida - %s, 0)
            WHERE id_instancia = %s
        """, (dano, id_inimigo_instancia))
        conn.commit()
    conn.close()


def remover_inimigos_mortos(id_pc):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM InstanciaInimigo WHERE id_pc = %s AND vida <= 0", (id_pc,))
        conn.commit()
    conn.close()

import random

def get_id_inimigo_por_instancia(id_instancia):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id_inimigo FROM InstanciaInimigo WHERE id_instancia = %s", (id_instancia,))
        resultado = cur.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def get_efeito_contra_inimigo(id_arma, id_inimigo):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT efeito_tipo
            FROM Arma_Efeito_Inimigo
            WHERE id_arma = %s AND id_inimigo = %s
        """, (id_arma, id_inimigo))
        resultado = cur.fetchone()
    conn.close()
    return resultado[0] if resultado else 'normal'


def inimigos_atacam(id_pc, personagem_id):
    inimigos = get_inimigos_no_pc(id_pc)
    for (id_instancia, nome, vida) in inimigos:
        if vida <= 0:
            continue
        id_inimigo = get_id_inimigo_por_instancia(id_instancia)  # busca id_inimigo da instância
        ataques = get_ataques_inimigo(id_inimigo)
        if not ataques:
            continue
        ataque = random.choice(ataques)
        chance = ataque[3]
        dano = ataque[2]
        nome_ataque = ataque[1]

        print(f"\nInimigo {nome} tenta usar {nome_ataque}!")
        if random.randint(1, 100) <= chance:
            aplicar_dano_personagem(personagem_id, dano)
            print(f"Inimigo acertou e causou {dano} de dano!")
        else:
            print("Inimigo errou o ataque!")


def get_ataques_inimigo(id_inimigo):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.id_ataque, a.nome, a.dano, a.chance_acerto
            FROM Ataque a
            JOIN Inimigo_Ataque ia ON ia.id_ataque = a.id_ataque
            WHERE ia.id_inimigo = %s
        """, (id_inimigo,))
        ataques = cur.fetchall()
    conn.close()
    return ataques


def aplicar_dano_personagem(personagem_id, dano):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE InstanciaEstagiario
            SET vida_atual = GREATEST(vida_atual - %s, 0)
            WHERE id_personagem = %s
        """, (dano, personagem_id))
        conn.commit()
    conn.close()


def personagem_morreu(personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT vida_atual FROM InstanciaEstagiario WHERE id_personagem = %s", (personagem_id,))
        vida = cur.fetchone()
    conn.close()
    return vida is None or vida[0] <= 0


def batalha_interface(id_pc, personagem_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Batalha (id_pc, id_personagem)
        VALUES (%s, %s)
        RETURNING id_batalha
    """, (id_pc, personagem_id))

        id_batalha = cur.fetchone()[0]
        conn.commit()
    conn.close()
    while True:
        limpar_tela()
        inimigos = get_inimigos_no_pc(id_pc)
        if not inimigos:
            print("Todos os inimigos foram derrotados! Parabéns!")
            break

        print("\n--- BATALHA ---")
        print("Inimigos detectados neste PC:")
        for idx, (id_instancia, nome, vida) in enumerate(inimigos, 1):
            print(f"  [{idx}] {nome} (HP: {vida})")

        # Menu principal
        print("\nO que você faz?")
        print("  [1] Atacar")
        print("  [2] Usar consumível")
        print("  [3] Usar power-up")
        print("  [4] Fugir")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            ataques = get_ataques_personagem(personagem_id)
            if not ataques:
                print("Você nem leu o livro de SQL básico, você acha mesmo que você consegue fazer algo?!")
                input("Pressione Enter para continuar...")

            if ataques:
                print("\nSeus ataques:")
                for idx, (id_ataque, nome, dano, chance) in enumerate(ataques, 1):
                    print(f"  [{idx}] {nome} (Dano: {dano}, Chance: {chance}%)")
                print("  [0] Voltar")

                escolha_ataque = input("Escolha seu ataque: ").strip()
                if escolha_ataque == "0":
                    continue
                if not escolha_ataque.isdigit() or not (1 <= int(escolha_ataque) <= len(ataques)):
                    print("Opção inválida.")
                    input("Pressione Enter para continuar...")
                    continue

                ataque_escolhido = ataques[int(escolha_ataque) - 1]
                id_ataque = ataque_escolhido[0]
                print("\nEscolha o inimigo para atacar:")
                for idx, (id_instancia, nome, vida) in enumerate(inimigos, 1):
                    print(f"  [{idx}] {nome} (HP: {vida})")

                escolha_alvo = input("Digite o número do inimigo: ").strip()
                if not escolha_alvo.isdigit() or not (1 <= int(escolha_alvo) <= len(inimigos)):
                    print("Alvo inválido.")
                    input("Pressione Enter para continuar...")
                    continue

                id_inimigo_instancia = inimigos[int(escolha_alvo) - 1][0]

                #Testar acerto
                if random.randint(1, 100) <= ataque_escolhido[3]:
                    atacar_inimigo(id_ataque, id_inimigo_instancia)
                    print("Você acertou o ataque!")
                else:
                    print("Você errou o ataque!")

                remover_inimigos_mortos(id_pc)

            #Turno dos inimigos
            inimigos_atacam(id_pc, personagem_id)
            if personagem_morreu(personagem_id):
                call_db_function('diminuir_respeito', personagem_id, 15)
                print("O Computador deu tela azul e nunca mais voltou...!")
                break
            input("Pressione Enter para continuar...")
        elif escolha == "2":
            usar_consumivel(personagem_id)
        elif escolha == "3":
            usar_power_up(personagem_id)
        elif escolha == "4":
            print("Você fugiu da batalha! Perdeu 5 de respeito.")
            call_db_function('diminuir_respeito', personagem_id, 5)
            break
        else:
            print("Opção inválida.")
            input("Pressione Enter para continuar...")
