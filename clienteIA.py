import urllib.request, sys, random, time


######################FUNÇÕES PARA EXECUTAR IA (MiniMax): #############################################

def miniMax(tabuleiro, nivel, jogador): #nivel máximo = 80

    filhos = []
    h = heuristica(tabuleiro, nivel)

    if(h != 0 or nivel == 0): #SE nó é um nó terminal OU profundidade = 0 ENTÃO
        return h, tabuleiro

    elif(jogador == 1):                       #SENÃO SE maximizador é FALSE ENTÃO
        minimo = inf                         #α ← +∞
        escolhido = tabuleiro
        filhos = abreTabuleiro(tabuleiro, jogador)
        for filho in filhos:                   #PARA CADA filho DE nó
            var, tab = miniMax(filho, nivel-1, 2)
            if(var < minimo):
                minimo = var                   #α ← min(α, minimax(filho, profundidade-1,true))
                escolhido = filho
        return minimo, escolhido               #RETORNE α

    elif(jogador == 2):                        #SENÃO //Maximizador
        maximo = -inf                         #α ← -∞
        escolhido = tabuleiro
        filhos = abreTabuleiro(tabuleiro, jogador)
        for filho in filhos:                   #PARA CADA filho DE nó
            var, tab = miniMax(filho, nivel-1, 1)   
            if(var > maximo):
                maximo = var                   #α ← max(α, minimax(filho, profundidade-1,false))
                escolhido = filho
        return maximo, escolhido

def abreTabuleiro(tabuleiro, jogador): #gera todas as jogadas possíveis naquele ponto
    
    x = 0
    y = 0
    filhos = []

    while(x < 11):
        if(x == 0 or x == 10):
            while(y < 5):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))
                y = y + 1
        elif(x == 1 or x == 9):
            while(y < 6):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))   
                y = y + 1
        elif(x == 2 or x == 8):
            while(y < 7):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))
                y = y + 1
        elif(x == 3 or x == 7):
            while(y < 8):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))
                y = y + 1
        elif(x == 4 or x == 6):
            while(y < 9):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))
                y = y + 1
        elif(x == 5):
            while(y < 10):
                if(tabuleiro[x][y] == 0):
                    filhos.append(jogada(copy.deepcopy(tabuleiro), jogador, x, y))
                y = y + 1
        y = 0
        x = x + 1

    return filhos

def heuristica(tabuleiro, nivel):        #retorna o valor da heurística daquele tabuleiro (0 = empate, 1 = jogador 1 ganha, -1 = jogador 2 (computador) ganha)
    
    j = Game()
    j.init_board()
    j.board = tabuleiro

    if(j.is_final_state() == None):
        return 0
    elif(j.is_final_state() == 1):
        return 1
    elif(j.is_final_state() == 2):
        return -1
    
def posicao(tabatual, escolhido):

    x = 0
    y = 0
    escx = 0
    escy = 0
    print('entrou pra escolher posicao')

    while(x < 11):
        if(x == 0 or x == 10):
            while(y < 5):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        elif(x == 1 or x == 9):
            while(y < 6):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        elif(x == 2 or x == 8):
            while(y < 7):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        elif(x == 3 or x == 7):
            while(y < 8):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        elif(x == 4 or x == 6):
            while(y < 9):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        elif(x == 5):
            while(y < 10):
                if(tabatual[x][y] != escolhido[x][y]):
                    escx = x
                    escy = y
                y = y + 1
        y = 0
        x = x + 1
    
    return escx, escy

def jogada(tabuleiro, jogador, x, y):

    tabuleiro[x][y] = jogador
    return tabuleiro



#########CLIENTE: (adaptado de random_client.py) ###############################################



if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        # Escolhe um movimento aleatoriamente
        movimento = random.choice(movimentos)

        # Pega tabuleiro:
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        tabuleiro = eval(resp.read())

        #APLICA MINIMAX E GERA O MOVIMENTO:

        valor, escolhido = miniMax(tabuleiro, len(movimentos), player)
        c, l = posicao(tabuleiro, escolhido)
        coluna = int(c)
        linha = int(l)
        print('posicao escolhida: ')
        print(coluna)
        print(linha)

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,coluna+1,linha+1))
        msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
    
    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)