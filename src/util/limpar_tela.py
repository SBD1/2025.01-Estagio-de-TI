import os
def limpar_tela():
    #Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')
