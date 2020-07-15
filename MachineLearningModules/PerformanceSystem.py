#######################################################################
# File name: PerformanceSystem.py                                     #
# Author: PhilipBasaric                                               #
#                                                                     #
# Description: Performance System of a Checkers machine-learning AI.  #
# Contains the methods that generate a game trace with move selection #
# performed by a supplied target function hypothesis. This module     #
# contains the hard-coded game logic define by the game of checkers.  #           
#                                                                     #
#######################################################################


import random, time, copy

# This is the performance system object. It is responsible for producing the game trace used by the critic module
class PerformanceSystem:

    # This function performs all actions that constitute a turn
    def runGame(self, gameState, v1, v2):
        # Update game state attributes
        gameState.info = [len(gameState.blackPieces), len(gameState.redPieces), len(gameState.blackKings), len(gameState.redKings), len(gameState.redThreat), len(gameState.blackThreat)] 
        self.move(gameState, v1, v2)
        # If one side has no pieces, game is over 
        if len(gameState.redPieces) == 0 and len(gameState.redKings) == 0 or len(gameState.blackPieces) == 0 and len(gameState.blackKings) == 0:
            gameState.isOver = True

    # Simple function that outputs the contents of the checkers board to the console 
    def drawBoard(self, board):
        print()
        print(" ", end=" ")
        for k in range(0,8):
            print(k, end="")
            print(" ", end="")
        print("")
        for i in range(0,len(board)):
            print(i, end=" ")
            for j in range(0,len(board)):
                print(board[i][j], end=" ")
            print("")

    # This function performs a move for a given player 
    def move(self, gameState, v1, v2):
        # Get set of legal moves with current board state
        legalMoves = self.getLegalMoves(gameState.currentTurn, gameState.redPieces, gameState.blackPieces, gameState.redKings, gameState.blackKings, gameState.redThreat, gameState.blackThreat,
                                   gameState.board) 
        # Check for stalemate 
        if len(legalMoves) == 0:
            gameState.isOver = True
            return 
        # Else proceed by obtaining and making the best move
        else:
            bestMove = self.getBestMove(gameState, legalMoves, v1, v2) # get the best move from legalMoves
            self.makeMove(gameState, bestMove) # make the best move using bestMove
        
    # This function probes every move and returns a 2D list containing the set of legal moves
    def getLegalMoves(self, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
        legalMoves = [] # array to be returned

        # Call getKingMoves - logic for King function 
        self.getKingMoves(legalMoves, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board)
        
        # The following code block accounts for all possible moves on the red player's side of the board
        if currentTurn == "red":
            for piece in redPieces:
                # move UP and to the RIGHT
                if (piece[0] - 1) > -1 and (piece[1] + 1) < 8: # check bounds
                    # Regular diagonal
                    if board[piece[0] - 1][piece[1] + 1] == " ": 
                        legalMoves.append([redPieces.index(piece), piece[0]-1, piece[1]+1, -1, "regular", "None"])
                    # Elimination
                    if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                        # Regular Elimination
                        if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]-1, piece[1]+1)
                            redThreat.append(threat) 
                            legalMoves.append([redPieces.index(piece), piece[0]-2, piece[1]+2, threat, "regular", "regular"])
                        # King Elimination
                        if board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(blackKings, piece[0]-1, piece[1]+1)
                            redThreat.append(threat) 
                            legalMoves.append([redPieces.index(piece), piece[0]-2, piece[1]+2, threat, "regular", "king"])
                # move UP and to the LEFT
                if (piece[0] - 1) > -1 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] - 1][piece[1] - 1] == " ": 
                        legalMoves.append([redPieces.index(piece), piece[0]-1, piece[1]-1, -1, "regular", "None"])
                    # Elimination
                    if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]-1, piece[1]-1)
                            redThreat.append(threat) 
                            legalMoves.append([redPieces.index(piece), piece[0]-2, piece[1]-2, threat, "regular", "regular"])
                        # King Elimination 
                        if board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(blackKings, piece[0]-1, piece[1]-1)
                            redThreat.append(threat) 
                            legalMoves.append([redPieces.index(piece), piece[0]-2, piece[1]-2, threat, "regular", "king"])

        # The following code block accounts for all possible moves on the black player's side of the board
        elif currentTurn == "black": 
             for piece in blackPieces:
                 # move DOWN and to the RIGHT
                if (piece[0] + 1) < 8 and (piece[1] + 1) < 8: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] + 1] == " ": 
                        legalMoves.append([blackPieces.index(piece), piece[0]+1, piece[1]+1, -1, "regular", "None"])
                    # Elimination
                    if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "r" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(redPieces, piece[0]+1, piece[1]+1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackPieces.index(piece), piece[0]+2, piece[1]+2, threat, "regular", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "R" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(redKings, piece[0]+1, piece[1]+1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackPieces.index(piece), piece[0]+2, piece[1]+2, threat, "regular", "king"])
                # move DOWN and to the LEFT
                if (piece[0] + 1) < 8 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] - 1] == " ": 
                        legalMoves.append([blackPieces.index(piece), piece[0]+1, piece[1]-1, -1, "regular", "None"])
                    # Elimination
                    if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(redPieces, piece[0]+1, piece[1]-1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackPieces.index(piece), piece[0]+2, piece[1]-2, threat, "regular", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(redKings, piece[0]+1, piece[1]-1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackPieces.index(piece), piece[0]+2, piece[1]-2, threat, "regular", "king"])
        return legalMoves

    # Helper function to getLegalMoves - details game code for King behaviour
    def getKingMoves(self, legalMoves, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
        # For red player
        if currentTurn == "red":
            for piece in redKings:
                # move UP and to the RIGHT
                if (piece[0] - 1) > -1 and (piece[1] + 1) < 8: # check bounds
                    # Regular diagonal
                    if board[piece[0] - 1][piece[1] + 1] == " ":
                        legalMoves.append([redKings.index(piece), piece[0]-1, piece[1]+1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                        # Regular elimination
                        if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]-1, piece[1]+1)
                            redThreat.append(threat) 
                            legalMoves.append([redKings.index(piece), piece[0]-2, piece[1]+2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(blackKings, piece[0]-1, piece[1]+1)
                            redThreat.append(threat) 
                            legalMoves.append([redKings.index(piece), piece[0]-2, piece[1]+2, threat, "king", "king"])
                # move UP and to the LEFT
                if (piece[0] - 1) > -1 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] - 1][piece[1] - 1] == " ": 
                        legalMoves.append([redKings.index(piece), piece[0]-1, piece[1]-1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]-1, piece[1]-1)
                            redThreat.append(threat) 
                            legalMoves.append([redKings.index(piece), piece[0]-2, piece[1]-2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(blackKings, piece[0]-1, piece[1]-1)
                            redThreat.append(threat) 
                            legalMoves.append([redKings.index(piece), piece[0]-2, piece[1]-2, threat, "king", "king"])
                # move DOWN and to the RIGHT
                if (piece[0] + 1) < 8 and (piece[1] + 1) < 8: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] + 1] == " ": 
                        legalMoves.append([redKings.index(piece), piece[0]+1, piece[1]+1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "b" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]+1, piece[1]+1)
                            redThreat.append(threat) # add black threat
                            legalMoves.append([redKings.index(piece), piece[0]+2, piece[1]+2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "B" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(blackKings, piece[0]+1, piece[1]+1)
                            redThreat.append(threat) # add black threat
                            legalMoves.append([redKings.index(piece), piece[0]+2, piece[1]+2, threat, "king", "king"])
                # move DOWN and to the LEFT
                if (piece[0] + 1) < 8 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] - 1] == " ": 
                        legalMoves.append([redKings.index(piece), piece[0]+1, piece[1]-1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "b" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(blackPieces, piece[0]+1, piece[1]-1)
                            redThreat.append(threat) # add black threat
                            legalMoves.append([redKings.index(piece), piece[0]+2, piece[1]-2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "B" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(blackKings, piece[0]+1, piece[1]-1)
                            redThreat.append(threat) # add black threat
                            legalMoves.append([redKings.index(piece), piece[0]+2, piece[1]-2, threat, "king", "king"])

        elif currentTurn == "black":
            for piece in blackKings:
                # move UP and to the RIGHT
                if (piece[0] - 1) > -1 and (piece[1] + 1) < 8: # check bounds
                    # Regular diagonal
                    if board[piece[0] - 1][piece[1] + 1] == " ": 
                        legalMoves.append([blackKings.index(piece), piece[0]-1, piece[1]+1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                        # Regular Elimination
                        if board[piece[0] - 1][piece[1] + 1] == "r" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(redPieces, piece[0]-1, piece[1]+1)
                            blackThreat.append(threat) 
                            legalMoves.append([blackKings.index(piece), piece[0]-2, piece[1]+2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] - 1][piece[1] + 1] == "R" and board[piece[0] - 2][piece[1] + 2] == " ":
                            threat = self.getIndex(redKings, piece[0]-1, piece[1]+1)
                            blackThreat.append(threat) 
                            legalMoves.append([blackKings.index(piece), piece[0]-2, piece[1]+2, threat, "king", "king"])
                # move UP and to the LEFT
                if (piece[0] - 1) > -1 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] - 1][piece[1] - 1] == " ": 
                        legalMoves.append([blackKings.index(piece), piece[0]-1, piece[1]-1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] - 1][piece[1] - 1] == "r" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(redPieces, piece[0]-1, piece[1]-1)
                            blackThreat.append(threat) 
                            legalMoves.append([blackKings.index(piece), piece[0]-2, piece[1]-2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] - 1][piece[1] - 1] == "R" and board[piece[0] - 2][piece[1] - 2] == " ":
                            threat = self.getIndex(redKings, piece[0]-1, piece[1]-1)
                            blackThreat.append(threat) 
                            legalMoves.append([blackKings.index(piece), piece[0]-2, piece[1]-2, threat, "king", "king"])
                # move DOWN and to the RIGHT
                if (piece[0] + 1) < 8 and (piece[1] + 1) < 8: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] + 1] == " ": 
                        legalMoves.append([blackKings.index(piece), piece[0]+1, piece[1]+1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "r" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(redPieces, piece[0]+1, piece[1]+1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackKings.index(piece), piece[0]+2, piece[1]+2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] + 1] == "R" and board[piece[0]+2][piece[1]+2] == " ":
                            threat = self.getIndex(redKings, piece[0]+1, piece[1]+1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackKings.index(piece), piece[0]+2, piece[1]+2, threat, "king", "king"])
                # move DOWN and to the LEFT
                if (piece[0] + 1) < 8 and (piece[1] - 1) > -1: # check bounds
                    # Regular Diagonal
                    if board[piece[0] + 1][piece[1] - 1] == " ": 
                        legalMoves.append([blackKings.index(piece), piece[0]+1, piece[1]-1, -1, "king", "None"])
                    # Diagonal Elimination
                    if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                        # Regular Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(redPieces, piece[0]+1, piece[1]-1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackKings.index(piece), piece[0]+2, piece[1]-2, threat, "king", "regular"])
                        # King Elimination
                        if board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                            threat = self.getIndex(redKings, piece[0]+1, piece[1]-1)
                            blackThreat.append(threat) # add black threat
                            legalMoves.append([blackKings.index(piece), piece[0]+2, piece[1]-2, threat, "king", "king"])

    # This is a helper function to getLegalMoves - It retrives the index of the piece that has been eliminated
    def getIndex(self, pieces, i, j):
        for piece in pieces:
            if piece[0] == i and piece[1] == j:
                return pieces.index(piece) # return the index of the piece that has been eliminated
        return None
                
    # This function retrives the best move from legalMoves using the target function hypothesis
    def getBestMove(self, gameState, legalMoves, v1, v2):
        rand = random.randint(3,4)
        if rand % 2 == 0:
            return legalMoves[random.randint(0,len(legalMoves)-1)]
        prediction = []
        bestMove = []
        if len(legalMoves) == 1:
            return legalMoves[0]
        for move in legalMoves:
            if gameState.currentTurn == "red":
                prediction.append(self.getPrediction(gameState, move, v1))
            elif gameState.currentTurn == "black":
                prediction.append(self.getPrediction(gameState, move, v2))
        maxVal = max(prediction)
        for move in legalMoves:
            if gameState.currentTurn == "red":
                if self.getPrediction(gameState, move, v1) == maxVal:
                    bestMove = move
            elif gameState.currentTurn == "black":
                if self.getPrediction(gameState, move, v2) == maxVal:
                    bestMove = move
        return bestMove
        
    # This function gets the output of the target hypothesis evaluated at the game state that succeeds a given move
    def getPrediction(self, gameState, move, v):
        # get blackThreat and redThreat by calling the functions
        if gameState.currentTurn == "red":
            v4 = v[4]*self.getRedThreat(gameState, move)
            v5 = v[5]*len(gameState.blackThreat)
        elif gameState.currentTurn == "black":
            v5 = v[5]*self.getBlackThreat(gameState, move)
            v4 = v[4]*len(gameState.redThreat)

        # Logic for red
        if gameState.currentTurn == "red":
            if move[4] == "regular":
                if move[1] == 0:
                    v1 = v[1]*len(gameState.redPieces) - 1
                    v3 = v[3]*len(gameState.redKings) + 1
                else:
                    v1 = v[1]*len(gameState.redPieces)
                    v3 = v[3]*len(gameState.redKings)
            elif move[4] == "king":
                v1 = v[1]*len(gameState.redPieces)
                v3 = v[3]*len(gameState.redKings)
            if move[5] == "None":
                v0 = v[0]*len(gameState.blackPieces)
                v2 = v[2]*len(gameState.blackKings)
            elif move[5] == "regular":
                v0 = v[0]*len(gameState.blackPieces) - 1
                v2 = v[2]*len(gameState.blackKings)
            elif move[5] == "king":
                v0 = v[0]*len(gameState.blackPieces)
                v2 = v[2]*len(gameState.blackKings) - 1

        # Logic for black
        elif gameState.currentTurn == "black":
            if move[4] == "regular":
                if move[1] == 0:
                    v1 = v[1]*len(gameState.blackPieces) - 1
                    v3 = v[3]*len(gameState.blackKings) + 1
                else:
                    v1 = v[1]*len(gameState.blackPieces)
                    v3 = v[3]*len(gameState.blackKings)
            elif move[4] == "king":
                v1 = v[1]*len(gameState.blackPieces)
                v3 = v[3]*len(gameState.blackKings)
            if move[5] == "None":
                v0 = v[0]*len(gameState.redPieces)
                v2 = v[2]*len(gameState.redKings)
            elif move[5] == "regular":
                v0 = v[0]*len(gameState.redPieces) - 1
                v2 = v[2]*len(gameState.redKings)
            elif move[5] == "king":
                v0 = v[0]*len(gameState.redPieces)
                v2 = v[2]*len(gameState.redKings) - 1
        val = v0 + v1 + v2 + v3 + v4 + v5
        return val

    # This function finds the number of black pieces threatned by red for a given hypothetical move
    def getRedThreat(self, gameState, move):
        board = gameState.board
        i = move[1]
        j = move[2]
        redThreat = 0
        # Make deep copies to avoid aliasing issues 
        tempRedPieces = copy.deepcopy(gameState.redPieces) 
        tempRedKings = copy.deepcopy(gameState.redKings)

        # Make hypothetical move
        if move[4] == "regular":
            tempRedPieces[move[0]] = [i, j] # update location of piece
        elif move[4] == "king":
            tempRedKings[move[0]] = [i, j] # update location of piece

        # Scan the board for threats made by regular red pieces
        for piece in tempRedPieces:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
            # check UP and to the LEFT
            if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
    
        # Scan the board for threats made by red kings         
        for piece in tempRedKings:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
            # check UP and to the LEFT
            if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
            # check DOWN and to the RIGHT
            if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] + 1][piece[1] + 1] == "b" and board[piece[0]+2][piece[1]+2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] + 1][piece[1] + 1] == "B" and board[piece[0]+2][piece[1]+2] == " ":
                    redThreat = redThreat + 1
            # check DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "b" and board[piece[0]+2][piece[1]-2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "B" and board[piece[0]+2][piece[1]-2] == " ":
                    redThreat = redThreat + 1
        return redThreat

    # This function finds the number of red pieces threatned by black for a given hypothetical move
    def getBlackThreat(self, gameState, move):
        board = gameState.board
        i = move[1]
        j = move[2]
        blackThreat = 0
        # Make deep copies to avoid aliasing issues 
        tempBlackPieces = copy.deepcopy(gameState.blackPieces)
        tempBlackKings = copy.deepcopy(gameState.blackKings)
        
        # Make hypothetical move
        if move[4] == "regular":
            tempBlackPieces[move[0]] = [i, j] # update location of piece
        elif move[4] == "king":
            tempBlackKings[move[0]] = [i, j] # update location of piece

        # Scan the board for threats made by regular black pieces 
        for piece in tempBlackPieces:
            # check DOWN and to the RIGHT
            if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] + 1][piece[1] + 1] == "r" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] + 1] == "R" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
            # check DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1

        # Scan the board for threats made by black kings   
        for piece in tempBlackKings:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "r" and board[piece[0] - 2][piece[1] + 2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "R" and board[piece[0] - 2][piece[1] + 2] == " ":
                    blackThreat = blackThreat + 1
            # check UP and to the LEFT
            if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] - 1][piece[1] - 1] == "r" and board[piece[0] - 2][piece[1] - 2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] - 1][piece[1] - 1] == "R" and board[piece[0] - 2][piece[1] - 2] == " ":
                    blackThreat = blackThreat + 1
            # move DOWN and to the RIGHT
            if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] + 1][piece[1] + 1] == "r" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] + 1] == "R" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
            # check DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
        return blackThreat
    
    # This function makes a given move by updating the game board, the pieces lists, and removing any eliminated pieces
    def makeMove(self, gameState, move):
        i = move[1] # row position of target location on board
        j = move[2] # column position of target location on board
        if gameState.currentTurn == "red":
            if move[4] == "regular":
                # Regular Diagonal
                if move[3] == -1:
                    gameState.board[i][j] = "r"
                    gameState.board[gameState.redPieces[move[0]][0]][gameState.redPieces[move[0]][1]] = " " # add whitespace to previous position
                    gameState.redPieces[move[0]][0] = i # update row position of red piece
                    gameState.redPieces[move[0]][1] = j # update column position of red piece
                # Elimination 
                elif move[3] > -1:
                    # Regular Elimination
                    if move[5] == "regular":
                        gameState.board[i][j] = "r"
                        gameState.board[gameState.redPieces[move[0]][0]][gameState.redPieces[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.blackPieces[move[3]][0]][gameState.blackPieces[move[3]][1]] = " "
                        gameState.blackPieces.pop(move[3])
                        gameState.redPieces[move[0]][0] = i # update row position of red piece
                        gameState.redPieces[move[0]][1] = j # update column position of red piece
                    # King Elimination
                    elif move[5] == "king": 
                        gameState.board[i][j] = "r"
                        gameState.board[gameState.redPieces[move[0]][0]][gameState.redPieces[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.blackKings[move[3]][0]][gameState.blackKings[move[3]][1]] = " "
                        gameState.blackKings.pop(move[3])
                        gameState.redPieces[move[0]][0] = i # update row position of red piece
                        gameState.redPieces[move[0]][1] = j # update column position of red piece
                # Promotion to king
                if i == 0:
                    gameState.board[i][j] = "R"
                    gameState.redKings.append(gameState.redPieces[move[0]]) # add a new red king
                    gameState.redPieces.pop(move[0]) # remove the promoted piece from redPieces
            if move[4] == "king":
                if move[3] == -1: # No piece being eliminated
                    gameState.board[i][j] = "R"
                    gameState.board[gameState.redKings[move[0]][0]][gameState.redKings[move[0]][1]] = " " # add whitespace to previous position
                    gameState.redKings[move[0]][0] = i # update row position of red piece
                    gameState.redKings[move[0]][1] = j # update column position of red piece
                else:
                    # Regular Elimination
                    if move[5] == "regular":
                        gameState.board[i][j] = "R"
                        gameState.board[gameState.redKings[move[0]][0]][gameState.redKings[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.blackPieces[move[3]][0]][gameState.blackPieces[move[3]][1]] = " "
                        gameState.blackPieces.pop(move[3])
                        gameState.redKings[move[0]][0] = i # update row position of red piece
                        gameState.redKings[move[0]][1] = j # update column position of red piece
                    # King Elimination
                    elif move[5] == "king":
                        gameState.board[i][j] = "R"
                        gameState.board[gameState.redKings[move[0]][0]][gameState.redKings[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.blackKings[move[3]][0]][gameState.blackKings[move[3]][1]] = " "
                        gameState.blackKings.pop(move[3])
                        gameState.redKings[move[0]][0] = i # update row position of red piece
                        gameState.redKings[move[0]][1] = j # update column position of red piece
            gameState.currentTurn = "black"    
        elif gameState.currentTurn == "black":
            if move[4] == "regular":
                # Regular Diagonal
                if move[3] == -1: 
                    gameState.board[i][j] = "b"
                    gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " " # add whitespace to previous position
                    gameState.blackPieces[move[0]][0] = i # update row position of red piece
                    gameState.blackPieces[move[0]][1] = j # update column position of red piece
                else:
                    # Regular Elimination   
                    if move[5] == "regular":
                        gameState.board[i][j] = "b"
                        gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.redPieces[move[3]][0]][gameState.redPieces[move[3]][1]] = " "
                        gameState.redPieces.pop(move[3])
                        gameState.blackPieces[move[0]][0] = i # update row position of red piece
                        gameState.blackPieces[move[0]][1] = j # update column position of red piece
                    # King Elimination 
                    elif move[5] == "king":
                        gameState.board[i][j] = "b"
                        gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " " # add whitespace to previous position
                        gameState.board[gameState.redKings[move[3]][0]][gameState.redKings[move[3]][1]] = " "
                        gameState.redKings.pop(move[3])
                        gameState.blackPieces[move[0]][0] = i # update row position of red piece
                        gameState.blackPieces[move[0]][1] = j # update column position of red piece
                # Promotion to king
                if i == 7:
                    gameState.board[i][j] = "B"
                    gameState.blackKings.append(gameState.blackPieces[move[0]]) # add a new black king
                    gameState.blackPieces.pop(move[0]) # remove black piece
            if move[4] == "king":
                if move[3] == -1: # No piece being eliminated
                    gameState.board[i][j] = "B"
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " " # add whitespace to previous position
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
                # Regular Elimination
                if move[5] == "regular":
                    gameState.board[i][j] = "B"
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " " # add whitespace to previous position
                    gameState.board[gameState.redPieces[move[3]][0]][gameState.redPieces[move[3]][1]] = " "
                    gameState.redPieces.pop(move[3])
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
                # King Elimination
                elif move[5] == "king":
                    gameState.board[i][j] = "B"
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " " # add whitespace to previous position
                    gameState.board[gameState.redKings[move[3]][0]][gameState.redKings[move[3]][1]] = " "
                    gameState.redKings.pop(move[3])
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
            gameState.currentTurn = "red"
                        
    # This function takes as input an initial board state and function hypothesis and produces a list containing the game trace for a given game 
    def getTrace(self, trainingExperiment, currentHypothesis1, currentHypothesis2):
        redTraceHistory = []
        blackTraceHistory = []
        board = copy.deepcopy(trainingExperiment)
        v1 = copy.deepcopy(currentHypothesis1)
        v2 = copy.deepcopy(currentHypothesis2)
        # 2D List containing red pieces and their positions on the above board
        redPieces = [
                [5, 1],
                [5, 3],
                [5, 5],
                [5, 7],
                [6, 0],
                [6, 2],
                [6, 4],
                [6, 6],
                [7, 1],
                [7, 3],
                [7, 5],
                [7, 7],  
            ]
        # 2D List containing black pieces and their positions on the above board
        blackPieces = [
                [0, 0],
                [0, 2],
                [0, 4],
                [0, 6],
                [1, 1],
                [1, 3],
                [1, 5],
                [1, 7],
                [2, 0],
                [2, 2],
                [2, 4],
                [2, 6],  
            ]
        redKings = [] # List of red kings is empty at game start
        blackKings = [] # List of black kings is empty at game start 
        redThreat = [] # List of black pieces threatned by red is empty at game start
        blackThreat = [] # List of red pieces threatned by black is empty at game start
        currentTurn = "red" # Assume red always goes first at start of game
        gameState = GameState(currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board) # Instantiate the initial game state
        while gameState.isOver == False: # Keep iterating until game is over
            if gameState.currentTurn == "red":
                redTraceHistory.append(gameState.info)
            elif gameState.currentTurn == "black":
                blackTraceHistory.append(gameState.info)
            if len(redTraceHistory) > 10000: # Impose hard limit on number of turns 
                break
            self.runGame(gameState, v1, v2)
        if gameState.currentTurn == "red":
            redTraceHistory.append(gameState.info)
        elif gameState.currentTurn == "black":
            blackTraceHistory.append(gameState.info)
        return [redTraceHistory, blackTraceHistory]
