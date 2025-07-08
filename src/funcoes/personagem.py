"""
Sistema de Personagens - Funcionalidades relacionadas à criação e gestão de personagens
"""
import time
from database import call_db_function, get_all_characters, get_connection

def criar_personagem():
    """Cria um novo personagem no jogo"""
    print("--- CRIAÇÃO DE PERSONAGEM ---\n")
    nome = input("Digite o nome do seu personagem: ").strip()

    if not nome:
        print("\nO nome não pode ser vazio. Tente novamente.")
        time.sleep(2)
        return False

    # Chama a função SQL para criar o personagem
    mensagem = call_db_function('criar_personagem', nome)
    print(f"\n{mensagem}")
    time.sleep(3)
    return True

def selecionar_personagem():
    """Permite ao jogador selecionar um personagem existente"""
    print("--- SELEÇÃO DE PERSONAGEM ---\n")
    print("Personagens disponíveis:\n")

    personagens = get_all_characters()

    if not personagens:
        print("Nenhum personagem criado ainda.")
        print("Por favor, crie um personagem no menu principal primeiro.")
        time.sleep(3)
        return None

    for char_id, char_name in personagens:
        print(f"[{char_id}] - {char_name}")

    try:
        escolha = int(input("\nDigite o ID do personagem: "))
        # Verifica se a escolha é um ID válido
        personagem_selecionado = next((p for p in personagens if p[0] == escolha), None)

        if not personagem_selecionado:
            raise ValueError

        return personagem_selecionado

    except (ValueError, IndexError):
        print("\nOpção inválida.")
        time.sleep(2)
        return None

def listar_personagens():
    """Lista todos os personagens com informações detalhadas"""
    personagens = get_all_characters()
    
    if not personagens:
        print("Nenhum personagem encontrado no sistema.")
        return
    
    print("\n============================================================")
    print("LISTA DE PERSONAGENS")
    print("============================================================")
    
    conn = get_connection()
    if not conn:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return
    
    try:
        with conn.cursor() as cur:
            for char_id, char_name in personagens:
                # Busca informações detalhadas do personagem
                cur.execute("""
                    SELECT p.nome, s.nome as sala_nome, s.id_sala
                    FROM personagem p
                    LEFT JOIN sala s ON p.id_sala = s.id_sala
                    WHERE p.id_personagem = %s;
                """, (char_id,))
                
                detalhes = cur.fetchone()
                
                if detalhes:
                    nome, sala_nome, id_sala = detalhes
                    print(f"\n👤 {nome} (ID: {char_id})")
                    print(f"   📍 Localização: {sala_nome or 'Desconhecida'} (ID: {id_sala or 'N/A'})")
                else:
                    print(f"\n👤 {char_name} (ID: {char_id})")
                    print(f"   ❌ Erro ao carregar detalhes")
    
    except Exception as e:
        print(f"Erro ao listar personagens: {e}")
    finally:
        conn.close()
    
    print("\n============================================================")

def excluir_personagem():
    """Permite excluir um personagem existente"""
    personagens = get_all_characters()
    
    if not personagens:
        print("Nenhum personagem encontrado para excluir.")
        return False
    
    print("\n--- EXCLUSÃO DE PERSONAGEM ---\n")
    print("Personagens disponíveis para exclusão:\n")
    
    for char_id, char_name in personagens:
        print(f"[{char_id}] - {char_name}")
    
    try:
        escolha = int(input("\nDigite o ID do personagem para excluir (0 para cancelar): "))
        
        if escolha == 0:
            print("Operação cancelada.")
            return False
        
        # Verifica se a escolha é um ID válido
        personagem_selecionado = next((p for p in personagens if p[0] == escolha), None)
        
        if not personagem_selecionado:
            print("ID inválido.")
            return False
        
        # Confirmação
        nome_personagem = personagem_selecionado[1]
        confirmacao = input(f"\nTem certeza que deseja excluir '{nome_personagem}'? (s/N): ").strip().lower()
        
        if confirmacao != 's':
            print("Operação cancelada.")
            return False
        
        # Executa a exclusão
        conn = get_connection()
        if not conn:
            print("Erro: Não foi possível conectar ao banco de dados.")
            return False
        
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM personagem WHERE id_personagem = %s;", (escolha,))
                
                if cur.rowcount > 0:
                    conn.commit()
                    print(f"\nPersonagem '{nome_personagem}' excluído com sucesso!")
                    return True
                else:
                    print("Erro: Personagem não encontrado.")
                    return False
                    
        except Exception as e:
            print(f"Erro ao excluir personagem: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
            
    except ValueError:
        print("Digite um número válido.")
        return False

def mover_personagem_para_sala(personagem_id, id_sala_destino):
  
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Verifica se a sala de destino existe
            cur.execute("SELECT nome FROM sala WHERE id_sala = %s;", (id_sala_destino,))
            sala = cur.fetchone()
            nome_sala = sala[0]
            
            # Verifica se o personagem existe
            cur.execute("SELECT nome FROM personagem WHERE id_personagem = %s;", (personagem_id,))
            personagem = cur.fetchone()
            nome_personagem = personagem[0]
            
            # Move o personagem
            cur.execute("UPDATE personagem SET id_sala = %s WHERE id_personagem = %s;", 
                       (id_sala_destino, personagem_id))
            
            if cur.rowcount > 0:
                conn.commit()
                print(f"Personagem '{nome_personagem}' movido para '{nome_sala}' com sucesso!")
                return True
                
    except Exception as e:
        print(f"Erro ao mover personagem: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
