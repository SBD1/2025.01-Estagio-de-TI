# src/dialogos.py

"""
Este arquivo centraliza todos os diálogos do jogo.
A estrutura é um dicionário onde a chave é o ID do personagem (NPC).

Cada NPC tem um dicionário com diferentes "estados" de diálogo:
- 'missao_disponivel': Diálogo que oferece uma missão.
- 'missao_em_andamento': O que o NPC diz enquanto a missão está ativa.
- 'missao_concluida': Diálogo após completar a missão.
- 'padrao': Diálogo geral, caso nenhuma outra condição seja atendida.
"""

DIALOGOS = {
    # --- Severino (ID: 1) ---
    # Missão: Vírus no Sistema (ID: 1) e Check-up no Servidor (ID: 7)
    1: {
        'missao_disponivel': {
            1: [
                "Estagiário! Que bom que você apareceu!",
                "Estou a detetar umas anomalias na rede... Parece que fomos infetados por um Malware.",
                "Preciso que encontre e elimine o foco da infeção antes que se espalhe. Pode fazer isso?"
            ],
            7: [
                "Ufa, ainda bem que te encontrei. O ar aqui não está gelado o suficiente?",
                "Um dos nossos racks principais, o Rack 03, está a sobreaquecer. Se ele parar, a empresa toda para.",
                "Não posso sair daqui. Poderia ir até à sala do Data Center e reiniciar o servidor para mim? É uma tarefa simples, mas crítica!"
            ]
        },
        'missao_em_andamento': {
            1: "O Malware ainda está ativo! Rápido, antes que os danos sejam maiores!",
            7: "O Rack 03 ainda está em perigo. Por favor, vá até o Data Center e faça a manutenção."
        },
        'padrao': "Mantenha os servidores a funcionar, esse é o lema. O ar condicionado no máximo, sempre!"
    },

    # --- João, o Almoxarife (ID: 2) ---
    # Missão: Hardware Novo (ID: 6)
    2: {
        'missao_disponivel': {
            6: [
                "Ah, o estagiário novo. Tenho uma tarefa para si, se não se importar de sujar as mãos.",
                "O pessoal do suporte no 2º andar está a precisar de umas peças novas com urgência.",
                "Pode levar estas caixas para eles? Cuidado, são frágeis. E pesadas. Boa sorte."
            ]
        },
        'missao_em_andamento': {
            6: "As peças ainda não chegaram ao destino? O pessoal do suporte vai ter um ataque se não as receber logo."
        },
        'padrao': "Mais caixas a chegar, mais coisas para catalogar. O trabalho de um almoxarife nunca acaba."
    },

    # --- Maria, a Recepcionista (ID: 3) ---
    # Missão: Network Inicial (ID: 3)
    3: {
        'missao_disponivel': {
            3: [
                "Olá, seja bem-vindo à nossa empresa! O meu nome é Maria.",
                "Vejo que é o novo estagiário de TI. Parabéns!",
                "Uma dica: a chave para o sucesso aqui é conhecer as pessoas certas. Que tal começar por se apresentar ao pessoal aqui do rés do chão? Um bom networking abre muitas portas."
            ]
        },
        'missao_em_andamento': {
            3: "Isso aí, seja simpático! Já falou com toda a gente por aqui?"
        },
        'padrao': "Bem-vindo! Se precisar de ajuda para localizar algum setor, é só falar comigo."
    },

    # --- Cláudio (ID: 4) ---
    4: {
        'padrao': "Viu o Severino por aí? Ele estava preocupado com a temperatura do Rack 03. Espero que não seja nada sério."
    },

    # --- Pedro (ID: 5) ---
    5: {
        'padrao': "Um dia, todas estas prateleiras estarão organizadas. Hoje não é esse dia. Nem amanhã, provavelmente."
    },
    
    # --- Raimunda (ID: 6) ---
    6: {
        'padrao': "Brrr, está um frio aqui que até os pinguins usavam casaco. Mas é ótimo para os servidores!"
    },
    
    # --- Cristiano (ID: 7) ---
    7: {
        'missao_disponivel': {
            2: [
                "Estagiário! Preciso da sua ajuda. O sistema acabou de ir para produção e está a explodir com bugs.",
                "São pequenos, mas irritantes. Parecem baratas digitais. E estão por todo o lado!",
                "Por favor, vasculhe o código e esmague esses bugs por mim. O chefe vai arrancar a minha pele se descobrir isto."
            ]
        },
        'missao_em_andamento': {
            2: "Já eliminou os bugs? Cada segundo que passa, mais um cliente reclama. Depressa!"
        },
        'padrao': "Café... preciso de mais café. E menos bugs. Principalmente menos bugs."
    },
    
    # --- Manoel (ID: 8) ---
    8: {
        'padrao': "Procura alguma coisa? Se não estiver na minha lista, oficialmente não existe. E provavelmente, mesmo que esteja, perdi."
    },

    # --- Ana (ID: 9) ---
    9: {
        'missao_disponivel': {
            5: [
                "(Você encontra uma programadora com o olhar perdido, a tremer ligeiramente)",
                "Café... preciso... de... café...",
                "Estou há três dias a tentar fechar uma task. Não consigo pensar. Por favor, traga-me um café da cafeteria. Qualquer um serve. O mais forte que houver!"
            ]
        },
        'missao_em_andamento': {
            5: "A...inda... sem... cafeína... o código... está a ficar... desfocado..."
        },
        'padrao': "A diferença entre um bom programador e um ótimo programador é a qualidade do seu café."
    },

    # --- Breno, o Barista (ID: 10) ---
    10: {
        'missao_disponivel': {
            8: [
                "Bom dia! Vai um cafezinho? ...Ah, se ao menos eu tivesse pão de queijo para acompanhar.",
                "Acredita que alguém anda a 'pedir emprestado' os meus pães de queijo? O stock some misteriosamente!",
                "Você parece um bom detetive. Se descobrir quem é o 'ladrão de pão de queijo', dou-lhe uma recompensa!"
            ]
        },
        'missao_em_andamento': {
            8: "Alguma pista sobre o caso do pão de queijo desaparecido? Estou de olho em toda a gente..."
        },
        'padrao': "O melhor café da cidade, modéstia à parte. Aceita um expresso?"
    },
    
    # --- Carlos, o Dev (ID: 11) ---
    11: {
        'inicio': [
            "(Você aproxima-se de um desenvolvedor com olheiras profundas, a digitar furiosamente)",
            "Não posso parar agora... o deploy é para hoje... o que é que quer?"
        ],
        'missao_alvo': [
            "Pão de queijo? Eu... eu não sei de nada. Porque está a olhar para mim assim?",
            "(Ele desvia o olhar para um guardanapo engordurado na mesa dele)",
            "Ok, ok, fui eu! Mas foi por uma boa causa! Estou há 48 horas acordado para entregar este projeto.",
            "Tome, pode levar o último de volta... e não conte a ninguém, por favor!"
        ],
        'padrao': "Só mais uma linha de código... ou talvez duzentas."
    },
    
    # --- Sargento Silva (ID: 12) ---
    12: {
        'missao_disponivel': {
            9: [
                "Estagiário. Apresente-se. Sargento Silva, chefe de segurança.",
                "Temos uma violação. Uma firewall foi mal configurada e pacotes de dados não autorizados estão a inundar a nossa rede.",
                "A sua missão, caso decida aceitar: vá para as trincheiras digitais e elimine esses pacotes. Conto consigo."
            ]
        },
        'missao_em_andamento': {
            9: "A ameaça ainda não foi neutralizada. Mexa-se, soldado!"
        },
        'padrao': "A segurança é como o oxigénio. Quando se tem, não se nota. Quando não se tem, é tarde demais."
    }
}