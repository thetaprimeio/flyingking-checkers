####################################
# File name: Generalizer.py
# Author: BenjaminBeggs
# 
# Description: Generalizer of a Checkers machine-learning AI. 
# Takes in a 2D array storing the game state [n][0] and the
# target function training value [0][n] and updates the
# weighting coefficients for the hypothesis target function.
#
# Weighting coefficient limits of [2, 2, 4, 4, 8, 8] are imposed
# by a sensitivity based updating rule.
#
####################################

import copy
from ComputeEquation import ComputeEquation

class Generalizer:
    @staticmethod
    def updateHypothesis(trainingExamples, currentHypothesis):
        updatedHypothesis = [None] * 6
        # Set limits on coefficient magnitudes
        coeffLim = [2, 2, 4, 4, 8, 8]
        # Sensitivity factor set at 0.001, other values may be used
        sensitivityFactor = 0.001;
        for i in range (0, len(trainingExamples)):
            tempArray = trainingExamples[i][0]
            updatedHypothesis[0] = currentHypothesis[0] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[0])
            updatedHypothesis[1] = currentHypothesis[1] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[1])
            updatedHypothesis[2] = currentHypothesis[2] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[2])
            updatedHypothesis[3] = currentHypothesis[3] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[3])
            updatedHypothesis[4] = currentHypothesis[4] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[4])
            updatedHypothesis[5] = currentHypothesis[5] + sensitivityFactor*(trainingExamples[i][1]-ComputeEquation.computeEqn(trainingExamples[i][0], currentHypothesis))*(tempArray[5])
        
        # Round updated hypothesis values to truncate error
        # Values produced otherwise have more significant figures than model accuracy allows
        for i in range (0, 6):
            updatedHypothesis[i] = round(updatedHypothesis[i], 2)
        
        # Impose weighting coefficient limitations
        for j in range (0, 6):
            # Determine percentage increase from current->updated hypothesis
            weightVal = (updatedHypothesis[j] - currentHypothesis[j])/currentHypothesis[j]
            
            # Force coefficient change maximum at 1 or -1
            if weightVal > 1:
                weightVal = 1
            if weightVal < -1:
                weightVal = -1
            
            # Force upper/lower limit convergence
            if (currentHypothesis[j] + weightVal) > coeffLim[j]:
                currentHypothesis[j] = round(coeffLim[j], 2)
            if (currentHypothesis[j] + weightVal) < (-1*coeffLim[j]):
                currentHypothesis[j] = round(-1*coeffLim[j], 2)
            else:
                currentHypothesis[j] = round(currentHypothesis[j] + weightVal, 2)
            
        return currentHypothesis