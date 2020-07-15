####################################
# File name: Critic.py
# Author: JordanCurnew
# 
# Description: Critic module for Checkers machine-learning AI.
# Takes as an input the trace history of a checkers game
# and generates a set of hypothesis training values.
#
####################################

from ComputeEquation import ComputeEquation

class Critic:
    #Takes in the trace history and for each game history computes V_train(game state) and stores it in the 2D list trainingValues
    @staticmethod
    def generateTrainingValues(traceHistory, currentHypothesis):
        trainingValues = []
        for x in range(0, len(traceHistory)-1):
            output = ComputeEquation.computeEqn(traceHistory[x+1], currentHypothesis)
            trainingValues.append([traceHistory[x], output])
        return trainingValues