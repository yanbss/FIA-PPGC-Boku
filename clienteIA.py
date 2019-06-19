import urllib.request, sys, random, time, copy
from math import inf

######################FUNÇÕES PARA EXECUTAR IA (MiniMax): #############################################

def miniMax(tabuleiro, nivel, jogador, nivelMax, parte): #nivel máximo = 80

    filhos = []
    h = heuristica(tabuleiro, nivel)

    if(h != 0 or nivel == nivelMax): #SE nó é um nó terminal OU profundidade = 0 ENTÃO
        return h, tabuleiro

    elif(jogador == 1):                       #SENÃO SE maximizador é FALSE ENTÃO
        minimo = inf                         #α ← +∞
        escolhido = tabuleiro
        filhos = get_available_moves(tabuleiro) #gera lista de jogadas, tem que botar no tabuleiro
        for filho in filhos:                   #PARA CADA filho DE nó
            x, y = filho
            #if(outroJogador(tabuleiro, x, jogador) == 0):
            if(filho in parte):
                t = copy.deepcopy(tabuleiro)
                t[x][y] = 1
                var, tab = miniMax(t, nivel-1, 2, nivelMax, parte)
                if(var < minimo):
                    minimo = var                   #α ← min(α, minimax(filho, profundidade-1,true))
                    escolhido = filho
        return minimo, escolhido               #RETORNE α

    elif(jogador == 2):                        #SENÃO //Maximizador
        maximo = -inf                         #α ← -∞
        escolhido = tabuleiro
        filhos = get_available_moves(tabuleiro)
        for filho in filhos:                   #PARA CADA filho DE nó
            x, y = filho
            #if(outroJogador(tabuleiro, x, jogador) == 0):
            if(filho in parte):
                t = copy.deepcopy(tabuleiro)
                t[x][y] = 2
                var, tab = miniMax(t, nivel-1, 1, nivelMax, parte)
                if(var > maximo):
                    maximo = var                   #α ← max(α, minimax(filho, profundidade-1,false))
                    escolhido = filho
        return maximo, escolhido


def heuristica(tabuleiro, nivel):        #retorna o valor da heurística daquele tabuleiro (0 = empate, 1 = jogador 1 ganha, -1 = jogador 2 (computador) ganha)
    
    if(is_final_state(tabuleiro) == None):
        return 0
    elif(is_final_state(tabuleiro) == 1):
        return -1 - nivel
    elif(is_final_state(tabuleiro) == 2):
        return 1 + nivel

    return 0

def outroJogador(tabuleiro, coluna, jogador):

    if(jogador == 1):
        outro = 2
    else:
        outro = 1

    for j in range(len(tabuleiro[coluna])):
        if(tabuleiro[coluna][j] == outro):
            return 1

    return 0


def geraTab(tabuleiro, parte):

    l = []

    if(parte == 'cima'):
        l = ((1,0),(2,0),(2,1),(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(5,4),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(8,0),(8,1),(9,0))
    if(parte == 'esquerda'):
        l = ((0,0),(0,1),(0,2),(0,3),(0,4),(1,1),(1,2),(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4))
    if(parte == 'baixo'):
        l = ((1,5),(2,5),(2,6),(3,5),(3,6),(3,7),(4,5),(4,6),(4,7),(4,8),(5,5),(5,6),(5,7),(5,8),(5,9),(6,5),(6,6),(6,7),(6,8),(7,5),(7,6),(7,7),(8,5),(8,6),(9,5))
    if(parte == 'direita'):
        l = ((6,4),(7,3),(7,4),(8,2),(8,3),(8,4),(9,1),(9,2),(9,3),(9,4),(10,0),(10,1),(10,2),(10,3),(10,4))
    return l


####################FUNÇÕES HERDADAS DE SERVER.PY PARA CÁLCULO DE HEURÍSTICA: ##################################

def neighbors(tabuleiro, coluna, linha):
        l = []

        if linha > 1:
            l.append((coluna, linha - 1))  # up
        else:
            l.append(None)

        if (coluna < 6 or linha > 1) and (coluna < len(tabuleiro)):
            if coluna >= 6:
                l.append((coluna + 1, linha - 1))  # upper right
            else:
                l.append((coluna + 1, linha))  # upper right
        else:
            l.append(None)
        if (coluna > 6 or linha > 1) and (coluna > 1):
            if coluna > 6:
                l.append((coluna - 1, linha))  # upper left
            else:
                l.append((coluna - 1, linha - 1))  # upper left
        else:
            l.append(None)

        if linha < len(tabuleiro[coluna - 1]):
            l.append((coluna, linha + 1))  # down
        else:
            l.append(None)

        if (coluna < 6 or linha < len(tabuleiro[coluna - 1])) and coluna < len(tabuleiro):
            if coluna < 6:
                l.append((coluna + 1, linha + 1))  # down right
            else:
                l.append((coluna + 1, linha))  # down right
        else:
            l.append(None)

        if (coluna > 6 or linha < len(tabuleiro[coluna - 1])) and coluna > 1:
            if coluna > 6:
                l.append((coluna - 1, linha + 1))  # down left
            else:
                l.append((coluna - 1, linha))  # down left
        else:
            l.append(None)

        return l

def is_final_state(tabuleiro):
    # test vertical

    global vitoria1, vitoria2

    for column in range(len(tabuleiro)):
        s = ""
        for line in range(len(tabuleiro[column])):
            state = tabuleiro[column][line]
            s += str(state)
            if vitoria1 in s:
                return 1
            if vitoria2 in s:
                return 2

    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
             (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            s += str(state)
            if vitoria1 in s:
                return 1
            if vitoria2 in s:
                return 2
            coords = neighbors(tabuleiro, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
             (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            s += str(state)
            if vitoria1 in s:
                return 1
            if vitoria2 in s:
                return 2
            coords = neighbors(tabuleiro, column, line)[4]

    return None

def get_available_moves(tabuleiro):
    l = []

    for column in range(len(tabuleiro)):
        for line in range(len(tabuleiro[column])):
            if(tabuleiro[column][line] == 0):
                l.append((column, line))

    return l

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

vitoria1 = "111"
vitoria2 = "222"

#Divide o tabuleiro em 4:

resp = urllib.request.urlopen("%s/tabuleiro" % host)
tab = eval(resp.read())

tabCima = geraTab(tab, 'cima')
tabEsquerda = geraTab(tab, 'esquerda')
tabBaixo = geraTab(tab, 'baixo')
tabDireita = geraTab(tab, 'direita')


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

        # Pega tabuleiro:
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        tab = eval(resp.read())

        #APLICA MINIMAX NAS 4 PARTES DO TABULEIRO E GERA O MOVIMENTO:

        if(is_final_state(tab) == 1):
        	print("Incrementou vitoria1")
        	vitoria1 += "1"
        if(is_final_state(tab) == 2):
        	print("Incrementou vitoria2")
        	vitoria2 += "2"

        tinicial = time.time()

        #valor, escolhido = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-2)

        valorCima, escolhidoCima = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabCima)
        valor = abs(valorCima)
        escolhido = escolhidoCima
        print('Fez tabela de cima')

        valorEsquerda, escolhidoEsquerda = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabEsquerda)
        if(abs(valorEsquerda) > valor and valorEsquerda != 0):
            valor = abs(valorEsquerda)
            escolhido = escolhidoEsquerda

        print('Fez tabela da esquerda')

        valorBaixo, escolhidoBaixo = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabBaixo)
        if(abs(valorBaixo) > valor and valorBaixo != 0):
            valor = abs(valorBaixo)
            escolhido = escolhidoBaixo

        print('Fez tabela de baixo')

        valorDireita, escolhidoDireita = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabDireita)
        if(abs(valorDireita) > valor and valorDireita != 0):
            valor = abs(valorDireita)
            escolhido = escolhidoDireita

        print('Fez tabela da direita')

        tfinal = time.time()
        print('Tempo total: ')
        print(tfinal - tinicial)

        coluna = escolhido[0]
        linha = escolhido[1]
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