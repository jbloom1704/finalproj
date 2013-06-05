'''
Game engine for the Tic-Tac-Toe agents.

'''

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
					
# Returns a list of position of squares, where each shows promise of k strikes horizontally					
def getRowWinningLineList(gamestate, forSymbol, m, n, k):
	winningSquareList = []
	for i in range(m):
		for j in range(n):
			if ((gamestate[i][j] == forSymbol) or (gamestate[i][j] == ' ')) and ((n - j)>=k): # if this square is a 'X' or 'O' and there are at least k squares ahead starting from j till n (both inclusive)
				ctr = j 
				obstacleFound = False
				while ctr <=(k-1) and (ctr < n):
					ctr+=1	
					if (gamestate[i][ctr] == '-') or (gamestate[i][ctr] == getAgainstSymbol(forSymbol)):
						obstacleFound = True
						break
	 		
				if (not obstacleFound):
					winningSquareList.append([i,j])
					
			elif (n-j) < k :  # Else if we have < k squares, then no need to explore further.
				break 
	return winningSquareList			
				
				
# Returns a list of positions of squares where each shows a promise of k strikes diagonally.				
def getDiagonalWinningList(gamestate, forSymbol, m, n, k, typeOfDiagonal):
	winningSquareList = []
	if typeOfDiagonal == 'clockwise' :
		for i in range(m):
			for j in range(n):
				if ((n - j) >= k) and ((m - i) >= k) and  ((gamestate[i][j] == forSymbol) or (gamestate[i][j] == ' ')):
					ctr_i = i 
					ctr_j = j
					obstacleFound = False
					while (ctr_i <= (k - 1)) and (ctr_j <= (k - 1)) and (ctr_i < m) and (ctr_j < n):
						if (gamestate[ctr_i][ctr_j] == '-') or (gamestate[ctr_i][ctr_j] == getAgainstSymbol(forSymbol)):
							obstacleFound = True
							break
						ctr_i+= 1
						ctr_j+= 1
					if not obstacleFound:
						winningSquareList.append([i, j])
				elif ((n - j) < k) or ((m - i) < k):
					break
					
	elif typeOfDiagonal == 'anticlockwise':
		i = 0
		j = n - 1
		while (i < m):
			while (j >=0):
				if (j >=(k - 1)) and ((m - i) >= k) and ((gamestate[i][j] == forSymbol) or (gamestate[i][j] == ' ')):
					ctr_i = i + 1
					ctr_j = j - 1 
					obstacleFound = False
					while (ctr_i <= (k -1)) and (ctr_j >= 0) and (ctr_i < m) :
						if (gamestate[ctr_i][ctr_j] == '-') or (gamestate[ctr_i][ctr_j] == getAgainstSymbol(forSymbol)):
							obstacleFound = True
							break
						ctr_i+= 1
						ctr_j-= 1
					if not obstacleFound:
						winningSquareList.append([i, j])
				elif (j < (k - 1)) or ((m - i) < k):
					break
				j-=1	
			i+=1
			j = n - 1
			
	return winningSquareList		
	
			
# Returns the string that introduces our agent	
def introduce():
	return "Good evening. My name is Sir Jonathan McCullen. I am here on behalf of my comrades to champion this gmae of yours called K-in-a-row-Tic-Tac-Toe."+\
			"I barely accept defeat and also claim position as one of the highest in the ranks of my lords "
			
# Returns the nickname of our agent			
def nickname():
	return "Sir McCullen"

#Initializes some of the global variables to prepare our agent for gameplay.	
def prepare(initial_state, k, what_side_I_play, opponent_nickname, mode='Normal'):
	global this_k
	this_k = k
	global side_I_play
	side_I_play = what_side_I_play	
	global oppon_nickname 
	oppon_nickname = opponent_nickname
	global this_mode 
	this_mode = mode
	global m
	global n
	global winningLineListX
	global winningLineListO
	global winningLineList
	m = len(initial_state[0])
	n = len(initial_state[0][0])
	iniZobristHash(m ,n) #Initialize zobrishHash with random numbers
	winningLineList  = getWinningLineList(initial_state, what_side_I_play, m, n, k)
	return "OK"


# Using Iterative Deepening and depth-first minimax alpha-beta search, returns the succesor, the move to attain it
# and a new remark describing the game state. 	
def makeMove(currState, currRemark, timeLimit = 10000):	
	global stats
	global this_k
	successor = currState
	move = [-1, -1]
	startTime = time.time()
	i = 1
	staticEvaluation = 0
	newRemark = "You gave me a finished game son"
	returnVal = [[move, currState], newRemark]

	#Begin Iterative deepening from 0 till 14 ply
	if (not isLeaf(currState)):
		while (i <= 30):
			stats[4] = i
			reqSuccessorPly = i
			successor, move, staticEvaluation = minmaxAlphaBeta(currState, [], i, -sys.maxsize, sys.maxsize)
			gameWinVerdict =  winTesterForK.winTesterForK(successor, move, this_k)
			endTime =  time.time()
			if (gameWinVerdict != "No win") or (((endTime - startTime) * 1000)  >=timeLimit):
				newRemark = getConvincingRemark(currState)
				returnVal = [[move, successor], newRemark]
				break	
			i+=1				
		returnVal = [[move, successor], newRemark]
	if returnVal[0][0] == [-1,-1]:
		returnVal = [None, newRemark]
	return returnVal
		
	
	
# Returns stats. Used when the Iterative Deepening in the  makeMove function is finished.	
def getStats():
	global stats
	return "depth reached "+str(stats[4])+" static evaluations "+str(stats[2])+", dynamic evaluations "+str(stats[3])+", alpha cutoff "+str(stats[0])+", beta cutoff "+str(stats[1])	

	
# Returns the static eval by computing static and dynamic evaluations by looking ahead down the tree.
# Uses alpha-beta pruning to discard any path of lower (higher)  interest	
def minmaxAlphaBeta(state, moveToAttainState, depth, alpha, beta):
	global stats	
	if depth != 0: 					         						
		stats[3]+=1          					# Increment the number of dynamic evaluation since we're at an interior node
	if  depth == 0 or (isLeaf(state)):
		stats[2]+=1 							# Increment the number of static evaluations since we're at a leaf or at the final depth
		return hashAndGetStaticEval(state, depth)	  #static evaluation (base case)
	successors, moves = successors_and_moves(state)		
	if state[1] == 'X':
		i = 0
		while i < len(successors): 
			alpha = max(alpha, minmaxAlphaBeta(successors[i], moves[i], depth - 1, alpha, beta))  
			if beta <= alpha:
				stats[1]+=1                 #Increment the number of beta cutoffs. 
				break   				# (* Beta cut-off *)
			i+=1
		if stats[4] == depth:               #If we are at the depth where we want to return the successor and the move required to attain it
			return [successors[i-1], moves[i-1], alpha]
		else:	
			return alpha	
	else:
		i = 0
		while i < len(successors):
			beta = min(beta, minmaxAlphaBeta(successors[i], moves[i], depth - 1, alpha, beta))     
			if beta <= alpha:
				stats[0]+=1                 # Increment the number of alpha cutoffs.
				break                           #  (* Alpha cut-off *)
			i+=1
		if stats[4] == depth:				#If we are at the depth where we want to return the successor and the move required to attain it
			return [successors[i-1], moves[i-1], beta]
		else:		
			return beta		
				
			
			
			
		
	
				
	

# Returns the static evaluation corresponding to this state and ply.
# If there is already a static evaluation to this state and ply in the zobrist hash
		# then return the corresponding static evaluation from zobrist hash
# else:
	#   do static evaluation corresponding to this state and ply and store it in the zobrish hash table.

# return the static_evaluation of this state	
def hashAndGetStaticEval(state, ply):	
	# Construct the zobrist key for this state
	stateKey = getStateKey(state)
	stateStaticEval = "a word"
	
	# Try getting the list of lists containing static_eval and ply corresponding to this state
	try:
		sePlyPairList = staticEvalDict[stateKey]  #sePlyPairList = [[ply1, static_eval1], [ply1, static_eval2] .....]
		for sePlyPair in sePlyPairList:
			if sePlyPair[0] == ply:
				stateStaticEval = sePlyPair[1]
				break
	except KeyError: 
		stateStaticEval = staticEval(state)
		staticEvalDict[stateKey] = [[ply, stateStaticEval]] #No such key existed. Therefore we create a new key for this state, and append [ply, stateStaticEval]
			
	if stateStaticEval is "a word": #If try block was executed and no static value was found, then we compute the static value and add [ply, stateStaticEval] to the existing key
		stateStaticEval = staticEval(state)
		staticEvalDict[stateKey].append([ply, stateStaticEval])
		
	return stateStaticEval	


	
		
# Returns true if this state is full (is a terminal node)		
def isLeaf(state):
	global m
	global n
	for i in range(m):
		for j in range(n):
			if state[0][i][j] == ' ': 
				return False
	return True		
				
				
#  Computes and returns a list containing a set of next-possible-states and a set of moves
# where each move reprents the x, y coordinate required to attain its corresponding state in the first list.
# Returns [[],[]] if the state is already full.
def successors_and_moves(state):
	global m
	global n
	sAndm = []
	coord = []
	if isLeaf(state):
		return [sAndm, coord]
	
	# Try to get the list of successors and moves from the list of squares where a winning line could actually start.
	for move in winningLineList:
		if (state[0][move[0]][move[1]] == ' ') and (not (move in coord)):
			temp = [[row[:] for row in state[0]]]
			if state[1] == 'X' :
				temp[0][move[0]][move[1]] = 'X' 
				temp.append('O')
			elif state[1] == 'O' :	
				temp[0][move[0]][move[1]] = 'O'  
				temp.append('X')
			sAndm.append(temp) 
			coord.append(move)
	
	# Else get the list of sucessors and moves from the empty spaces available.
	if (sAndm == []) and (coord == []):
		for i in range(m):
			for j in range(n):
				if(state[0][i][j] == ' '):
					temp = [[row[:] for row in state[0]]]
					temp[0][i][j] = state[1]
					temp.append(getAgainstSymbol(state[1])) #To make it similar to state, add the player symbol which is to be played for the next possible state.
					sAndm.append(temp)
					coord.append([i,j])
					
	return [sAndm, coord]	
	 	
		
# returns the static evaluation of this state.		
def staticEval(state):
	h1x = static_eval_rows(state[0], state[1]) #we only use the game state here and not the next player symbol	
	h1o = static_eval_rows(state[0], getAgainstSymbol(state[1]))
	
	#now transpose this game state to get a row view of the columns
	gamestate_transp = [list(i) for i in zip(*state[0])]
	h2x = static_eval_rows(gamestate_transp, state[1])
	h2o = static_eval_rows(gamestate_transp, getAgainstSymbol(state[1]))
		
	return (h1x + h2x) - (h1o + h2o)


# Retuns the static evaluation of a state with m Rows and n Columns
# Used as a HELPER FUNCTION for staticEval(state)
def static_eval_rows(gamestate, forSymbol):
	global n
	global this_k
	polynomial = 0
	for i in range(n):
		coeffCtr = 0
		for row in gamestate:
			#if (number_of_forSymbols_in_this_row == i) and ( AgainstSymbol and '-' are not in row)
			numEmptySpaces = row.count(' ') 
			numForSymbol = row.count(forSymbol)
			if (row.count(forSymbol) == i) and (numEmptySpaces >= this_k):
				coeffCtr+=1
				
		polynomial+= (10**i) * (coeffCtr)	
	return polynomial					
	

# Returns the symbol of the opponent	
def getAgainstSymbol(symbol):
	if(symbol == 'X'):
		return 'O'
	return 'X'	

# Returns the remark corresponding to the last makeMove() computation	
def getConvincingRemark(currState):
	global stats
	global side_I_play
	global m 
	global n
	global this_mode
	random 
	mySymbol = currState[1]
	ctrMySymb = ctrOpponSymb = ctrFr = ctrEm = 0
	for row in currState[0]:
		ctrMySymb+=row.count(mySymbol)
		ctrOpponSymb+=row.count(getAgainstSymbol(mySymbol))
		ctrFr+=row.count('-')
		ctrEm+=row.count(' ')
	if this_mode == 'Normal':	
		if ctrMySymb >= ctrOpponSymb and stats[2] < 30:
			return "Its only the beginning my friend and we lead the way with "+str(stats[3])	
		elif ctrMySymb >= ctrOpponSymb  and  ((stats[2] > 30 and stats[2] < 70)  or (random.random()> 0 and random.random() <  0.3)) :
			return	"Well sir, it seems our diligent "+str(ctrMySymb)+" men have discoverd some "+str(stats[2])+\
				" deepest inventions with "+str(stats[3])+" dynamic stategies. Scared, are you?"
		elif ctrMySymb >= ctrOpponSymb and ((stats[2] > 70 and stats[2] < 150) or (random.random()> 0.3 and random.random() <  0.6)):	
			return "It seems our "+str(ctrMySymb)+" men have more control now seeing that our "+\
			str(stats[1])+" beta cutoffs and "+str(stats[3])+" dynamic evaluations keeps growing by every move. "
			
		elif ctrMySymb >= ctrOpponSymb and ((stats[2] > 150 and stats[2] < 400) or (random.random()> 0.3 and random.random() < 0.9)) :	
			return "My "+str(ctrMySymb)+" men have taken goon control in the latter half of our game. I mean "+\
			str(stats[3])+" static evaluations and "+str(stats[2])+" beta cutoffs isnt bad after all. "
						
		elif ctrMySymb < ctrOpponSymb and stats[2] < 50:
			return "Ahh you think having larger forces will help you gain victory. Well not unless my  "+str(stats[2])+" static evals keep growing"
				
		elif ctrMySymb < ctrOpponSymb  and  ((stats[2] > 30 and stats[2] < 70)  or (random.random()> 0 and random.random() <  0.3))  :
			return	"Haha! You think outnumbering your men by "+str(ctrMySymb- ctrOpponSymb)+" will help you win? "+\
				"Well, not as long as ,"+str(stats[2])+" static evaluations and "+str(stats[1])+" shortcuts continue to aid us"
				
		elif ctrMySymb < ctrOpponSymb and ((stats[2] > 70 and stats[2] < 150) or (random.random()> 0.3 and random.random() <  0.6)):	
			return "It seems our "+str(ctrMySymb)+" have less control seeing that your "+\
			str(ctrOpponSymb)+" fools are scrambling for victory. You musn't forget I still have "+str(ctrEm)+" barre land to seize"+\
			"with ever increasing "+str(stats[2])+" static evaluations "
		
		elif ctrMySymb < ctrOpponSymb and ((stats[2] > 150 and stats[2] < 400) or (random.random()> 0.3 and random.random() < 0.9)):	
			return "With all the "+str(ctrFr)+" I am surprised "+str(ctrOpponSymb)+" tired leftover of yours "+\
			 " have managed to outnumber us. But "+str(stats[3])+" static evaluations and "+str(stats[2])+" beta cutoffs is definitely getting us ahead. "
			 
		elif (stats[2] > 200) and (ctrEm >=((m * n)/3)) :
			return "Looks like 1/3 of the board is already occupied and my "+str(ctrMySymb)+" are leading the way"
		
		elif stats[2] > 400 :
			return " Shoulnd't you give up? We already have "+str(stats[2])+" and "+str(ctrMySymb)+" leading the way "
			
		elif stats[2] > 600 :
			return "Looks like we're on a big game. Indeed with "+str(m)+"-by-"+str(n)+" board my "+str(stats[2])+" new methods find it very easy to"+\
					"traverse our way to victory "
		else:
			if side_I_play == 'X':
				return " I have "+str(stats[2])+" deep discoveries, "+str(stats[3])+" dynamic strategies and surprisingly  "+str(stats[1])+" shortcuts "+". All the"+\
						" more reasons for you to give up "
						
			return " I have "+str(stats[2])+" deep discoveries, "+str(stats[3])+" dynamic strategies, and surprisingly "+str(stats[0])+" shortcuts "+". All the"+\
						" more reasons for you to give up "
						
	elif this_mode == 'Static':
		return "currState static evaluation = "+str(staticEval(currState))
	elif this_mode == 'Dynamic':
		return getStats()
			
	 
	
	
