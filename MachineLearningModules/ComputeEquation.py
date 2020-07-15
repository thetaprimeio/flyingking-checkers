####################################
# File name: ComputeEquation.py
# Author: JordanCurnew
# 
# Description: Takes in an instance of a game state and 
# outputs the target function evaluated at that game state.
#
# Helper function used by other machine-learning modules.
# 
####################################

class ComputeEquation:
    @staticmethod
    def computeEqn(gameState, inputHypothesis):
        output = 0
        for i in range(0,6):
            output += inputHypothesis[i]*gameState[i]
        return output