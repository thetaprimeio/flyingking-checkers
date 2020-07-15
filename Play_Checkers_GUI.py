#######################################################################
# File name: PerformanceSystemHumanIO.py                              #
# Author: PhilipBasaric, JordanCurnew                                 #
#                                                                     #
# Description: PyQt5 Checkers GUI that loads a trained target         #
# function for the White enemy player. The Human player controls the  #
# black pieces.                                                       #
#                                                                     #
# Contains the Performance System for a Checkers machine-learning AI. #
# Contains the methods that generate a game trace with move selection #
# performed by a supplied target function hypothesis.                 #
#                                                                     #
# PyQt5 must be installed to run.                                     #
#                                                                     #
#######################################################################

import random, time, copy, sys, os

# Append project directories to system path
sys.path.append(os.getcwd() + '/MachineLearningModules')

# self class stores the state of the game at any given time (it stores variables described in textbook)
class GameState:
    # Constructor for GameState
    def __init__(self, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
        self.isOver = False # Boolean - true if game is over, false if not
        self.currentTurn = currentTurn # self stores the player whose current turn it is ("red" or "black")
        self.redPieces = redPieces # 2D list containing the red pieces
        self.blackPieces = blackPieces # 2D list containing the black pieces
        self.redKings = redKings
        self.blackKings = blackKings
        self.redThreat = redThreat # 1D list containing the black pieces THREATNED by red
        self.blackThreat = blackThreat # 1D list containing the red pieces THREATNED by black
        self.x1 = len(blackPieces) # x1 stores the number of black pieces on the board
        self.x2 = len(redPieces) # x2 stores the number of red pieces on the board
        self.x3 = len(redThreat) # x3 stores the number of black pieces THREATNED by red
        self.x4 = len(blackThreat) # x4 stores the number of red pieces THREATNED by black
        self.board = board  # Matrix of characters - represents the checkers board
        self.info = [len(self.blackPieces), len(self.redPieces), len(self.blackKings), len(self.redKings), len(self.redThreat), len(self.blackThreat)]

class PerformanceSystemHumanIO:

    #The below lists and functions are used for getting user input from the GUI
    selectedCheckersPiece = [0,0, "WAIT"]
    selectedBoardSpot = [-1,-1]

    #Function that is called when a checkers piece is clicked. Used to describe checkers piece location for 'yourMove' function
    def pickPiece(self, piece, boardWindow):
            self.selectedCheckersPiece[0] = int(piece[1])
            self.selectedCheckersPiece[1] = int(piece[2])
            if eval('boardWindow.' + piece + '.notchesVisible()') == True:
                    self.selectedCheckersPiece[2] = "King"
            else:
                    self.selectedCheckersPiece[2] = "Regular"


    #Function that is called when a board spot is clicked. Used to describe board location for 'yourMove' function
    def moveTo(self, boardselectedBoardSpot):
            self.selectedBoardSpot[0] = int(boardselectedBoardSpot[1])
            self.selectedBoardSpot[1] = int(boardselectedBoardSpot[2])

    #Mutator for selectedCheckersPiece list
    def setselectedCheckersPiece(self, new):
        self.selectedCheckersPiece = new

    #Mutator for selectedBoardSpot
    def setselectedBoardSpot(self, new):
        self.selectedBoardSpot = new


    # self function performs all actions that constitute a turn. It also displays the board upon each call
    def runGame(self, gameState, v):
        gameState.info = [len(gameState.blackPieces), len(gameState.redPieces), len(gameState.blackKings), len(gameState.redKings), len(gameState.redThreat), len(gameState.blackThreat)]
        #self.drawBoard(gameState.board)
        #app.exec_()
        self.move(gameState, v)
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

    # self function performs a move for a given player
    def move(self, gameState, v):
        legalMoves = self.getLegalMoves(gameState.currentTurn, gameState.redPieces, gameState.blackPieces, gameState.redKings, gameState.blackKings, gameState.redThreat, gameState.blackThreat,
                                   gameState.board) # get set of legal moves

        # If no moves can be made, end the game
        if len(legalMoves) == 0:
            gameState.isOver = True
            return
        # Otherwise, make a move
        else:
            bestMove = self.getBestMove(gameState, legalMoves, v) # get the best move from legalMoves
            self.makeMove(gameState, bestMove) # make the best move using bestMove


    # self function probes every move and returns a 2D list containing the set of legal moves
    def getLegalMoves(self, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
        legalMoves = [] # array to be returned

        # Call checkKing - logic for King function
        self.checkKing(legalMoves, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board)

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

    # self is a helper function to getLegalMoves - It retrives the index of the piece that has been eliminated
    def getIndex(self, pieces, i, j):
        for piece in pieces:
            if piece[0] == i and piece[1] == j:
                return pieces.index(piece) # return the index of the piece that has been eliminated
        return None

    # Helper function to getLegalMoves - details game code for King behaviour
    def checkKing(self, legalMoves, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
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

    #Allows the user to make a move using the GUI
    def yourMove(self, legalMoves, gameState):
        self.setselectedCheckersPiece([0,0,"WAIT"])
        self.setselectedBoardSpot([-1,-1])
        flag = True
        while flag == True:
            while self.selectedCheckersPiece[2] == "WAIT" or  self.selectedBoardSpot[0] == -1:
                QtCore.QCoreApplication.processEvents()


            if self.selectedCheckersPiece[2] == "Regular":
                index = self.getIndex(gameState.blackPieces, self.selectedCheckersPiece[0], self.selectedCheckersPiece[1])
            elif self.selectedCheckersPiece[2] == "King":
                index = self.getIndex(gameState.blackKings, self.selectedCheckersPiece[0], self.selectedCheckersPiece[1])

            for move in legalMoves:
                if move[0] == index and move[1] == self.selectedBoardSpot[0] and move[2] == self.selectedBoardSpot[1]:
                    flag = False
                    return legalMoves[legalMoves.index(move)]
            self.setGetselectedBoardSpot([-1,-1])
            continue

        return None



    # self function retrives the best move from legalMoves using the target function hypothesis
    def getBestMove(self, gameState, legalMoves, v):
        if gameState.currentTurn == "red":
            prediction = []
            for move in legalMoves:
               prediction.append(self.getPrediction(gameState, move, v))
            maxVal = max(prediction)
            for move in legalMoves:
                if self.getPrediction(gameState, move, v) == maxVal:
                    bestMove = move
        elif gameState.currentTurn == "black":
            bestMove = self.yourMove(legalMoves, gameState)
        return bestMove

    # self function gets the output of the target hypothesis evaluated at the game state that succeeds a given move
    def getPrediction(self, gameState, move, v):
        # get blackThreat and redThreat by calling the functions
        if gameState.currentTurn == "red":
            v4 = v[4]*self.getRedThreat(gameState, move)
            v5 = v[5]*len(gameState.blackThreat)
        elif gameState.currentTurn == "black":
            v5 = v[5]*self.getBlackThreat(gameState, move)
            v4 = v[4]*len(gameState.redThreat)
        # Check current turn
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
        # Check current turn
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

    # self function finds the number of black pieces threatned by red for a given hypothetical move
    def getRedThreat(self, gameState, move):
        board = gameState.board
        i = move[1]
        j = move[2]
        redThreat = 0
        tempRedPieces = copy.deepcopy(gameState.redPieces)
        tempRedKings = copy.deepcopy(gameState.redKings)
        # Make hypothetical move
        if move[4] == "regular":
            tempRedPieces[move[0]] = [i, j] # update location of piece
        # Make hypothetical move
        elif move[4] == "king":
            tempRedKings[move[0]] = [i, j] # update location of piece

        for piece in tempRedPieces:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
            # move UP and to the LEFT
            if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1

        for piece in tempRedKings:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "b" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "B" and board[piece[0] - 2][piece[1] + 2] == " ":
                    redThreat = redThreat + 1
            # move UP and to the LEFT
            if (piece[0] - 2) > -1 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] - 1][piece[1] - 1] == "b" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] - 1][piece[1] - 1] == "B" and board[piece[0] - 2][piece[1] - 2] == " ":
                    redThreat = redThreat + 1
            # move DOWN and to the RIGHT
            if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] + 1][piece[1] + 1] == "b" and board[piece[0]+2][piece[1]+2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] + 1][piece[1] + 1] == "B" and board[piece[0]+2][piece[1]+2] == " ":
                    redThreat = redThreat + 1
            # move DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "b" and board[piece[0]+2][piece[1]-2] == " ":
                    redThreat = redThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "B" and board[piece[0]+2][piece[1]-2] == " ":
                    redThreat = redThreat + 1
        return redThreat

    # self function finds the number of red pieces threatned by black for a given hypothetical move
    def getBlackThreat(self, gameState, move):
        board = gameState.board
        i = move[1]
        j = move[2]
        blackThreat = 0
        tempBlackPieces = copy.deepcopy(gameState.blackPieces)
        tempBlackKings = copy.deepcopy(gameState.blackKings)
        # Make hypothetical move
        if move[4] == "regular":
            tempBlackPieces[move[0]] = [i, j] # update location of piece
        # Make hypothetical move
        elif move[4] == "king":
            tempBlackKings[move[0]] = [i, j] # update location of piece

        # Scan the board for threats
        for piece in tempBlackPieces:
            # move DOWN and to the RIGHT
            if (piece[0] + 2) < 8 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] + 1][piece[1] + 1] == "r" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] + 1] == "R" and board[piece[0]+2][piece[1]+2] == " ":
                    blackThreat = blackThreat + 1
            # move DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1

        # Scan the board for threats
        for piece in tempBlackKings:
            # check UP and to the RIGHT
            if (piece[0] - 2) > -1 and (piece[1] + 2) < 8: # check double bounds
                if board[piece[0] - 1][piece[1] + 1] == "r" and board[piece[0] - 2][piece[1] + 2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] - 1][piece[1] + 1] == "R" and board[piece[0] - 2][piece[1] + 2] == " ":
                    blackThreat = blackThreat + 1
            # move UP and to the LEFT
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
            # move DOWN and to the LEFT
            if (piece[0] + 2) < 8 and (piece[1] - 2) > -1: # check double bounds
                if board[piece[0] + 1][piece[1] - 1] == "r" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
                elif board[piece[0] + 1][piece[1] - 1] == "R" and board[piece[0]+2][piece[1]-2] == " ":
                    blackThreat = blackThreat + 1
        return blackThreat

    # self function 'makes' the move by updating the board and deleting any eliminated pieces
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
                        gameState.board[gameState.redPieces[move[0]][0]][gameState.redPieces[move[0]][1]] = " "
                        gameState.board[gameState.blackPieces[move[3]][0]][gameState.blackPieces[move[3]][1]] = " "
                        gameState.blackPieces.pop(move[3])
                        gameState.redPieces[move[0]][0] = i # update row position of red piece
                        gameState.redPieces[move[0]][1] = j # update column position of red piece
                    # King Elimination
                    elif move[5] == "king":
                        gameState.board[i][j] = "r"
                        gameState.board[gameState.redPieces[move[0]][0]][gameState.redPieces[move[0]][1]] = " "
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
                        gameState.board[gameState.redKings[move[0]][0]][gameState.redKings[move[0]][1]] = " "
                        gameState.board[gameState.blackPieces[move[3]][0]][gameState.blackPieces[move[3]][1]] = " "
                        gameState.blackPieces.pop(move[3])
                        gameState.redKings[move[0]][0] = i # update row position of red piece
                        gameState.redKings[move[0]][1] = j # update column position of red piece
                    # King Elimination
                    elif move[5] == "king":
                        gameState.board[i][j] = "R"
                        gameState.board[gameState.redKings[move[0]][0]][gameState.redKings[move[0]][1]] = " "
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
                    gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " "
                    gameState.blackPieces[move[0]][0] = i # update row position of red piece
                    gameState.blackPieces[move[0]][1] = j # update column position of red piece
                else:
                    # Regular Elimination
                    if move[5] == "regular":
                        gameState.board[i][j] = "b"
                        gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " "
                        gameState.board[gameState.redPieces[move[3]][0]][gameState.redPieces[move[3]][1]] = " "
                        gameState.redPieces.pop(move[3])
                        gameState.blackPieces[move[0]][0] = i # update row position of red piece
                        gameState.blackPieces[move[0]][1] = j # update column position of red piece
                    # King Elimination
                    elif move[5] == "king":
                        gameState.board[i][j] = "b"
                        gameState.board[gameState.blackPieces[move[0]][0]][gameState.blackPieces[move[0]][1]] = " "
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
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " "
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
                # Regular Elimination
                if move[5] == "regular":
                    gameState.board[i][j] = "B"
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " "
                    gameState.board[gameState.redPieces[move[3]][0]][gameState.redPieces[move[3]][1]] = " "
                    gameState.redPieces.pop(move[3])
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
                # King Elimination
                elif move[5] == "king":
                    gameState.board[i][j] = "B"
                    gameState.board[gameState.blackKings[move[0]][0]][gameState.blackKings[move[0]][1]] = " "
                    gameState.board[gameState.redKings[move[3]][0]][gameState.redKings[move[3]][1]] = " "
                    gameState.redKings.pop(move[3])
                    gameState.blackKings[move[0]][0] = i # update row position of red piece
                    gameState.blackKings[move[0]][1] = j # update column position of red piece
            gameState.currentTurn = "red"

    def getTrace(self, trainingExperiment, currentHypothesis):


        traceHistory = []
        board = copy.deepcopy(trainingExperiment)
        v = copy.deepcopy(currentHypothesis)
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
        redKings = []
        blackKings = []
        redThreat = [] # List of black pieces threatned by red is empty at game start
        blackThreat = [] # List of red pieces threatned by black is empty at game start
        currentTurn = "red" # Assume red always goes first at start of game
        
        ######################
        # GUI Pertinent Code #
        ######################
        app = QApplication(sys.argv)
        boardWindow = CheckersGUIApplication()
        
        # Connect presses to corresponding functions
        boardWindow.w00.sliderPressed.connect(lambda: self.pickPiece("w00", boardWindow))
        boardWindow.w02.sliderPressed.connect(lambda: self.pickPiece("w02", boardWindow))
        boardWindow.w04.sliderPressed.connect(lambda: self.pickPiece("w04", boardWindow))
        boardWindow.w06.sliderPressed.connect(lambda: self.pickPiece("w06", boardWindow))
        boardWindow.w11.sliderPressed.connect(lambda: self.pickPiece("w11", boardWindow))
        boardWindow.w13.sliderPressed.connect(lambda: self.pickPiece("w13", boardWindow))
        boardWindow.w15.sliderPressed.connect(lambda: self.pickPiece("w15", boardWindow))
        boardWindow.w17.sliderPressed.connect(lambda: self.pickPiece("w17", boardWindow))
        boardWindow.w20.sliderPressed.connect(lambda: self.pickPiece("w20", boardWindow))
        boardWindow.w22.sliderPressed.connect(lambda: self.pickPiece("w22", boardWindow))
        boardWindow.w24.sliderPressed.connect(lambda: self.pickPiece("w24", boardWindow))
        boardWindow.w26.sliderPressed.connect(lambda: self.pickPiece("w26", boardWindow))
        boardWindow.w31.sliderPressed.connect(lambda: self.pickPiece("w31", boardWindow))
        boardWindow.w33.sliderPressed.connect(lambda: self.pickPiece("w33", boardWindow))
        boardWindow.w35.sliderPressed.connect(lambda: self.pickPiece("w35", boardWindow))
        boardWindow.w37.sliderPressed.connect(lambda: self.pickPiece("w37", boardWindow))
        boardWindow.w40.sliderPressed.connect(lambda: self.pickPiece("w40", boardWindow))
        boardWindow.w42.sliderPressed.connect(lambda: self.pickPiece("w42", boardWindow))
        boardWindow.w44.sliderPressed.connect(lambda: self.pickPiece("w44", boardWindow))
        boardWindow.w46.sliderPressed.connect(lambda: self.pickPiece("w46", boardWindow))
        boardWindow.w51.sliderPressed.connect(lambda: self.pickPiece("w51", boardWindow))
        boardWindow.w53.sliderPressed.connect(lambda: self.pickPiece("w53", boardWindow))
        boardWindow.w55.sliderPressed.connect(lambda: self.pickPiece("w55", boardWindow))
        boardWindow.w57.sliderPressed.connect(lambda: self.pickPiece("w57", boardWindow))
        boardWindow.w60.sliderPressed.connect(lambda: self.pickPiece("w60", boardWindow))
        boardWindow.w62.sliderPressed.connect(lambda: self.pickPiece("w62", boardWindow))
        boardWindow.w64.sliderPressed.connect(lambda: self.pickPiece("w64", boardWindow))
        boardWindow.w66.sliderPressed.connect(lambda: self.pickPiece("w66", boardWindow))
        boardWindow.w71.sliderPressed.connect(lambda: self.pickPiece("w71", boardWindow))
        boardWindow.w73.sliderPressed.connect(lambda: self.pickPiece("w73", boardWindow))
        boardWindow.w75.sliderPressed.connect(lambda: self.pickPiece("w75", boardWindow))
        boardWindow.w77.sliderPressed.connect(lambda: self.pickPiece("w77", boardWindow))
        boardWindow.s00.pressed.connect(lambda: self.moveTo("s00"))
        boardWindow.s02.pressed.connect(lambda: self.moveTo("s02"))
        boardWindow.s04.pressed.connect(lambda: self.moveTo("s04"))
        boardWindow.s06.pressed.connect(lambda: self.moveTo("s06"))
        boardWindow.s11.pressed.connect(lambda: self.moveTo("s11"))
        boardWindow.s13.pressed.connect(lambda: self.moveTo("s13"))
        boardWindow.s15.pressed.connect(lambda: self.moveTo("s15"))
        boardWindow.s17.pressed.connect(lambda: self.moveTo("s17"))
        boardWindow.s20.pressed.connect(lambda: self.moveTo("s20"))
        boardWindow.s22.pressed.connect(lambda: self.moveTo("s22"))
        boardWindow.s24.pressed.connect(lambda: self.moveTo("s24"))
        boardWindow.s26.pressed.connect(lambda: self.moveTo("s26"))
        boardWindow.s31.pressed.connect(lambda: self.moveTo("s31"))
        boardWindow.s33.pressed.connect(lambda: self.moveTo("s33"))
        boardWindow.s35.pressed.connect(lambda: self.moveTo("s35"))
        boardWindow.s37.pressed.connect(lambda: self.moveTo("s37"))
        boardWindow.s40.pressed.connect(lambda: self.moveTo("s40"))
        boardWindow.s42.pressed.connect(lambda: self.moveTo("s42"))
        boardWindow.s44.pressed.connect(lambda: self.moveTo("s44"))
        boardWindow.s46.pressed.connect(lambda: self.moveTo("s46"))
        boardWindow.s51.pressed.connect(lambda: self.moveTo("s51"))
        boardWindow.s53.pressed.connect(lambda: self.moveTo("s53"))
        boardWindow.s55.pressed.connect(lambda: self.moveTo("s55"))
        boardWindow.s57.pressed.connect(lambda: self.moveTo("s57"))
        boardWindow.s60.pressed.connect(lambda: self.moveTo("s60"))
        boardWindow.s62.pressed.connect(lambda: self.moveTo("s62"))
        boardWindow.s64.pressed.connect(lambda: self.moveTo("s64"))
        boardWindow.s66.pressed.connect(lambda: self.moveTo("s66"))
        boardWindow.s71.pressed.connect(lambda: self.moveTo("s71"))
        boardWindow.s73.pressed.connect(lambda: self.moveTo("s73"))
        boardWindow.s75.pressed.connect(lambda: self.moveTo("s75"))
        boardWindow.s77.pressed.connect(lambda: self.moveTo("s77"))

        gameState = GameState(currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board) # Instantiate the initial game state
        while gameState.isOver == False: # keep running until game is over
            readBoardState(boardWindow, gameState.board)
            # Update GUI display
            boardWindow.show()
            if gameState.currentTurn == "red":
                traceHistory.append(gameState.info)
            self.runGame(gameState, v)
        traceHistory.append(gameState.info)
        return traceHistory

######################
# GUI Pertinent Code #
######################
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import checkersBoard, pickle
from ExperimentGenerator import ExperimentGenerator

# Load the target hypothesis generated by training simulations
currentHypothesis = pickle.load(open(os.getcwd() + "/SavedValues/targetHypothesisRed.p", "rb" ))
if (len(currentHypothesis) != 6):
    raise ValueError('There is something unusual about the dimensions of the Pickle file read for the hypothesis state. Please inspect it.')

class CheckersGUIApplication(QtWidgets.QMainWindow, checkersBoard.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CheckersGUIApplication, self).__init__(parent)
        self.setupUi(self)

# Instantiate the GUI and show it
def main():
    expGen = ExperimentGenerator()
    perfSys = PerformanceSystemHumanIO()
    perfSys.getTrace(expGen.getExperiment(), currentHypothesis)

# Reads a board state encoded as a 2D array and updates the GUI canvas to replicate it
def readBoardState(boardWindow, boardState):
    for i in range(0, 8):
        for j in range (0, 8):
            if boardState[i][j] == "b":
                exec('boardWindow.b' + str(i) + str(j)  + '.setVisible(False)')
                exec('boardWindow.w' + str(i) + str(j)  + '.setVisible(True)')
                exec('boardWindow.w' + str(i) + str(j)  + '.setNotchesVisible(False)')
            elif boardState[i][j] == "r":
                exec('boardWindow.w' + str(i) + str(j)  + '.setVisible(False)')
                exec('boardWindow.b' + str(i) + str(j)  + '.setVisible(True)')
                exec('boardWindow.b' + str(i) + str(j)  + '.setNotchesVisible(False)')
            elif boardState[i][j] == "B":
                exec('boardWindow.b' + str(i) + str(j)  + '.setVisible(False)')
                exec('boardWindow.w' + str(i) + str(j)  + '.setVisible(True)')
                exec('boardWindow.w' + str(i) + str(j)  + '.setNotchesVisible(True)')
            elif boardState[i][j] == "R":
                exec('boardWindow.w' + str(i) + str(j)  + '.setVisible(False)')
                exec('boardWindow.b' + str(i) + str(j)  + '.setVisible(True)')
                exec('boardWindow.b' + str(i) + str(j)  + '.setNotchesVisible(True)')
            elif boardState[i][j] == " ":
                try:
                    exec('boardWindow.b' + str(i) + str(j)  + '.setVisible(False)')
                except:
                    pass
                try:
                    exec('boardWindow.w' + str(i) + str(j)  + '.setVisible(False)')
                except:
                    pass

# Force execution of main
if __name__ == '__main__':
    main()