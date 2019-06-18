import urllib.request, sys, random, time, copy
from math import inf

######################FUNÇÕES PARA EXECUTAR IA (MiniMax): #############################################

def miniMax(tabuleiro, nivel, jogador, nivelMax): #nivel máximo = 80

    filhos = []
    h = heuristica(tabuleiro)

    if(h != 0 or nivel == nivelMax): #SE nó é um nó terminal OU profundidade = 0 ENTÃO
    	return h, tabuleiro

    elif(jogador == 1):                       #SENÃO SE maximizador é FALSE ENTÃO
        minimo = inf                         #α ← +∞
        escolhido = tabuleiro
        filhos = get_available_moves(tabuleiro) #gera lista de jogadas, tem que botar no tabuleiro
        for filho in filhos:                   #PARA CADA filho DE nó
            x, y = filho
            if(outroJogador(tabuleiro, x, jogador) == 0):
	            t = copy.deepcopy(tabuleiro)
	            t[x][y] = 1
	            var, tab = miniMax(t, nivel-1, 2, nivelMax)
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
            if(outroJogador(tabuleiro, x, jogador) == 0):
	            t = copy.deepcopy(tabuleiro)
	            t[x][y] = 2
	            var, tab = miniMax(t, nivel-1, 1, nivelMax)
	            if(var > maximo):
	                maximo = var                   #α ← max(α, minimax(filho, profundidade-1,false))
	                escolhido = filho
        return maximo, escolhido


def heuristica(tabuleiro):        #retorna o valor da heurística daquele tabuleiro (0 = empate, 1 = jogador 1 ganha, -1 = jogador 2 (computador) ganha)
    
	#impedejogada = 0

	if(is_final_state(tabuleiro) == None):
		return 0
	elif(is_final_state(tabuleiro) == 1):
		return -1
	elif(is_final_state(tabuleiro) == 2):
		return 1

	'''
		for i in range (len(tabuleiro)):
			tamanhocoluna = len(tabuleiro[i])
			for j in range (tamanhocoluna):
				if(tabuleiro[i][j] == jogador):
					for k in range (tamanhocoluna): #testa se tem outro jogador naquela coluna
						if (tabuleiro[i][k] != jogador and tabuleiro[i][k] != 0): #se tiver, impede de jogar naquela coluna
							return 0
		if(jogador == 1):
			return 1
		if(jogador == 2):
			return -1
	'''

def outroJogador(tabuleiro, coluna, jogador):

	if(jogador == 1):
		outro = 2
	else:
		outro = 1

	for j in range(len(tabuleiro[coluna])):
		if(tabuleiro[coluna][j] == outro):
			return 1

	return 0

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
        for column in range(len(tabuleiro)):
            s = ""
            for line in range(len(tabuleiro[column])):
                state = tabuleiro[column][line]
                s += str(state)
                if "11111" in s:
                    return 1
                if "22222" in s:
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
                if "11111" in s:
                    return 1
                if "22222" in s:
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
                if "11111" in s:
                    return 1
                if "22222" in s:
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

        #APLICA MINIMAX E GERA O MOVIMENTO:

        tinicial = time.time()
        valor, escolhido = miniMax(copy.deepcopy(tab), len(movimentos), player, len(movimentos)-2)
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