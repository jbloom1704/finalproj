import random
import winTesterForK
import sys
import time
reqSuccessorPly = -1
this_k = 0
side_I_play = 'X'
oppon_nickname  = 'Bob'
this_mode = 'Dynamic'
zobristHash = []
staticEvalDict = {}
m = n = -1
winningLineList = []
stats = [0,0,0,0,-1]


# Initialize zobrist hashtable with values 
def iniZobristHash(rows, cols):
	global zobristHash
	zobristHash = [[[0 for i in range(4)] for j in range(n)] for z in range(m)]
	for i in range(rows):
		for j in range(cols):
			zobristHash[i][j][0] = random.randint(0, 4294967296) # for 'X'
			zobristHash[i][j][1] = random.randint(0, 4294967296) # for 'O'
			zobristHash[i][j][2] = random.randint(0, 4294967296) # for '-'
			zobristHash[i][j][3] = random.randint(0, 4294967296) # for ' '		

			
# Returns the deep index for the symbol in the zobristhash 
# Helper function for getStateKeyState(state)
def getIndexForSymbol(symbol):
	if symbol == 'X':
		return 0
	elif symbol == 'O':
		return 1
	elif symbol == '-':
		return 2
	return 3 #   symbol == ' '
			
# Returns the key corresponding to this state			
def getStateKey(state):
	global zobristHash
	key = 0
	for i in range(len(state[0])):
		for j in range(len(state[0][0])):
			whatIsAtIJ = state[0][i][j]
			key^=zobristHash[i][j][getIndexForSymbol(whatIsAtIJ)]
	return key			
	
	
# Returns a list of the positions of squares, where each one shows a promise of k strikes 
# horizontally or/and vertically or/and diagnonally in both ends			
def getWinningLineList(state, forSymbol, m, n, k):
	gamestate = state[0]
	rowWinningLineList = columnWinningLineList = diagonal1WinningLineList = diagonal2WinningLineList = []
	rowWinningLineList = getRowWinningLineList(gamestate, forSymbol, m, n, k)
	gamestate_transp = [list(i) for i in zip(*gamestate)] #
	columnWinningLineList = getRowWinningLineList(gamestate_transp, forSymbol, n, m, k)
	diagonal1WinningLineList = getDiagonalWinningList(gamestate, forSymbol, m, n, k, 'clockwise')
	diagonal2WinningLineList = getDiagonalWinningList(gamestate, forSymbol, n, n, k, 'anticlockwise')
	lst = rowWinningLineList + columnWinningLineList + diagonal1WinningLineList + diagonal2WinningLineList
	return lst
					
