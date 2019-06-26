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


def geraTab(tabuleiro, parte):

    l = []

    if(parte == 'cima'):
        l = [(1,0),(2,0),(2,1),(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(4,3),(5,0),(5,1),(5,2),(5,3),(5,4),(6,0),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(8,0),(8,1),(9,0)]
    if(parte == 'esquerda'):
        l = [(0,0),(0,1),(0,2),(0,3),(0,4),(1,1),(1,2),(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4)]
    if(parte == 'baixo'):
        l = [(1,5),(2,5),(2,6),(3,5),(3,6),(3,7),(4,5),(4,6),(4,7),(4,8),(5,5),(5,6),(5,7),(5,8),(5,9),(6,5),(6,6),(6,7),(6,8),(7,5),(7,6),(7,7),(8,5),(8,6),(9,5)]
    if(parte == 'direita'):
        l = [(6,4),(7,3),(7,4),(8,2),(8,3),(8,4),(9,1),(9,2),(9,3),(9,4),(10,0),(10,1),(10,2),(10,3),(10,4)]
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

    global ultima_jogada

    removal_options = can_remove(tabuleiro)
    if removal_options != None:
        return removal_options
    for column in range(len(tabuleiro)):
        for line in range(len(tabuleiro[column])):
            if(tabuleiro[column][line] == 0 and tabuleiro[column][line] != ultima_jogada):
                    l.append((column, line))
    return l

def can_remove(tabuleiro):
        removals = []
        l = []

        global last_column, last_line
        
        #test upward
        s = ""
        for line in range(max(last_line-3,1), last_line+1):
          
            state = tabuleiro[last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(last_column,last_line-1),(last_column,last_line-2)])

        #test downward
        s = ""
        for line in range(last_line,  min(last_line+3,len(tabuleiro[last_column-1]))+1):
        
            state = tabuleiro[last_column-1][line-1]
            s += str(state)
        
        if ("1221" in s and player==1) or ("2112" in s and player==2):
            removals.append([(last_column,last_line+1),(last_column,last_line+2)])
                 

        # test upward diagonals
        diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(tabuleiro, column, line)[1]
            if coords == None:
                break

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(tabuleiro, column, line)[5]
            if coords == None:
                break

        # test downward diagonals
        diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(tabuleiro, column, line)[2]
            if coords == None:
                break

        col = last_column
        line = last_line
        coords = (col, line)

        s = ""
        for i in range(0, 4):
            column = coords[0]
            line = coords[1]
            state = tabuleiro[column - 1][line - 1]
            l.append((column, line))
            s += str(state)
            if "1221" in s and player == 1:
                removals.append(l[-3:-1])
            if "2112" in s and player == 2:
                removals.append(l[-3:-1])
            coords = neighbors(tabuleiro, column, line)[4]
            if coords == None:
                break

        if len(removals) > 0:
            removals = [item for sublist in removals for item in sublist]
            return removals
        else:
            return None

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
block = None

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

        ######ARRUMAR PRA INCREMENTAR QUANDO TEM OUTRO JOGADOR QUE NAO ELE PROPRIO

        if(is_final_state(tab) == 1):
            print("Incrementou vitoria1")
            vitoria1 += "1"
        if(is_final_state(tab) == 2):
            print("Incrementou vitoria2")
            vitoria2 += "2"

        if(len(movimentos) > 2): #jogadas normais, sem remoção

            #APLICA MINIMAX NAS 4 PARTES DO TABULEIRO E GERA O MOVIMENTO:

            resp = urllib.request.urlopen("%s/ultima_jogada" % host) #pega a última jogada, para que não a repita no caso de ter sido peça eliminada
            ultima_jogada = eval(resp.read())

            last_column = ultima_jogada[0]
            last_line = ultima_jogada[1]

            tinicial = time.time()

            #PARA NÃO REPETIR JOGADA BLOQUEADA APÓS UMA REMOÇÃO:

            #if(ultima_jogada in tabCima):
            #    tabCima.remove(ultima_jogada)
            #if(ultima_jogada in tabEsquerda):
            #    tabEsquerda.remove(ultima_jogada)
            #if(ultima_jogada in tabBaixo):
            #    tabBaixo.remove(ultima_jogada)
            #if(ultima_jogada in tabDireita):
            #    tabBaixo.remove(ultima_jogada)

            #Testa o minimax nas 4 partes do tabuleiro e escolhe o que retornar uma jogada com o menor número de níveis abertos necessários
            
            valorCima, escolhidoCima = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabCima)
            valor = abs(valorCima)
            escolhido = escolhidoCima

            valorEsquerda, escolhidoEsquerda = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabEsquerda)
            if(abs(valorEsquerda) > valor and valorEsquerda != 0):
                valor = abs(valorEsquerda)
                escolhido = escolhidoEsquerda

            valorBaixo, escolhidoBaixo = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabBaixo)
            if(abs(valorBaixo) > valor and valorBaixo != 0):
                valor = abs(valorBaixo)
                escolhido = escolhidoBaixo

            valorDireita, escolhidoDireita = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-3, tabDireita)
            if(abs(valorDireita) > valor and valorDireita != 0):
                valor = abs(valorDireita)
                escolhido = escolhidoDireita

            tfinal = time.time()
            print('Tempo total: ')
            print(tfinal - tinicial)
            coluna = escolhido[0]
            linha = escolhido[1]

            #if(ultima_jogada in tabCima):
            #    tabCima.append(ultima_jogada)
            #if(ultima_jogada in tabEsquerda):
            #    tabEsquerda.append(ultima_jogada)
            #if(ultima_jogada in tabBaixo):
            #    tabBaixo.append(ultima_jogada)
            #if(ultima_jogada in tabDireita):
            #    tabBaixo.append(ultima_jogada)

        else: #jogada de remoção, escolhe um aleatório para remover
            coluna, linha = random.choice(movimentos)
            block = coluna, linha
            print('block: ')
            print(block)
            coluna -= 1
            linha -= 1

        print('posicao escolhida: ')
        print(coluna+1)
        print(linha+1)

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