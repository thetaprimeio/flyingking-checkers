#######################################################################
# File name: GameState.py                                             #
# Author: PhilipBasaric                                               #
#                                                                     #
# Description: The GameState object defines the state of a game.      #
# It stores all relevant game state attributes.                       #           
#                                                                     #
#######################################################################

class GameState:
    # Constructor for GameState 
    def __init__(self, currentTurn, redPieces, blackPieces, redKings, blackKings, redThreat, blackThreat, board):
        self.isOver = False # Used for determining whether game is over
        self.currentTurn = currentTurn # This stores the player whose current turn it is (stores literals: "red" or "black")
        self.redPieces = redPieces # 2D list containing the red pieces and their locations on the board
        self.blackPieces = blackPieces # 2D list containing the black pieces and their locations on the board
        self.redKings = redKings # 2D list containing the red kings and their locations on the board
        self.blackKings = blackKings # 2D list containing the black kings and their locations on the board
        self.redThreat = redThreat # 1D list containing the indeces of the black pieces THREATNED by red
        self.blackThreat = blackThreat # 1D list containing the indeces of the red pieces THREATNED by black
        self.board = board  # Matrix of characters - represents the checkers board
        self.info = [len(self.blackPieces), len(self.redPieces), len(self.blackKings), len(self.redKings), len(self.redThreat), len(self.blackThreat)] # list of attribute lengths - used in target function
