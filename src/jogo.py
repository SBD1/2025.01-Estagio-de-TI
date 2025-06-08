import psycopg2
import os


DB_NAME = "jogo_estagiario"
DB_USER = "postgres"
DB_PASSWORD = "lucas123"
DB_HOST = "localhost"

def conectar_bd():
        conexao = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password = 'lucas123', host=DB_HOST)
        return conexao
    

def obter_posicao_estagiario(cursor, estagiario_id):
    cursor.execute("""
        SELECT a.nome AS andar_nome, s.nome AS sala_nome, s.id_sala
        FROM Estagiario e
        JOIN Andar a ON e.andar_atual = a.id_andar
        JOIN Sala s ON s.id_andar = a.id_andar -- Assumindo que a sala é a sala principal do andar
        WHERE e.id_personagem = %s
    """, (estagiario_id,))
    return cursor.fetchone()

def mover_estagiario(cursor, estagiario_id, direcao_movimento):
    print(f"Tentando mover na direção: {direcao_movimento}")
    cursor.execute("SELECT andar_atual FROM Estagiario WHERE id_personagem = %s", (estagiario_id,))
    andar_atual_id = cursor.fetchone()[0]

    novo_andar_id = andar_atual_id # 

    if direcao_movimento == 'Norte':
        if andar_atual_id < 10: 
            novo_andar_id = andar_atual_id + 1
    elif direcao_movimento == 'Sul':
        if andar_atual_id > -2: 
            novo_andar_id = andar_atual_id - 1

    if novo_andar_id != andar_atual_id:
        cursor.execute("UPDATE Estagiario SET andar_atual = %s WHERE id_personagem = %s", (novo_andar_id, estagiario_id))
        print(f"Você se moveu para o andar {novo_andar_id}!")
    else:
        print("Você não pode ir nessa direção aqui.")




def jogo():
    conexao = conectar_bd()
    executor = conexao.cursor()
    estagiario_id = 1 

    while True:
        
        posicao = obter_posicao_estagiario(executor, estagiario_id)
        if posicao:
            print(f"Você está no {posicao[0]}, na {posicao[1]}.")
            print("O que você quer fazer? (W/A/S/D para mover, Q para sair)")
        else:
            print("Estagiário não encontrado!")
            break

        comando = input("> ").upper()

        if comando == 'Q':
            print("Saindo do jogo. Até a próxima!")
            break
        elif comando in ['W', 'A', 'S', 'D']:
            direcoes = {'W': 'Norte', 'S': 'Sul', 'A': 'Oeste', 'D': 'Leste'}
            mover_estagiario(executor, estagiario_id, direcoes[comando])
            conexao.commit() 
        else:
            print("Comando inválido. Tente novamente.")

        

    executor.close()
    conexao.close()

if __name__ == "__main__":
    jogo()