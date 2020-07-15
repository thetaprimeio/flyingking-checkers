####################################
# File name: ExperimentGenerator.py
# Author: BenjaminBeggs
# 
# Description: Experiment Generator for a Checkers machine-learning AI. 
# Generates a training experiment for the machine-learning process
# and stores the active state of the target function hypothesis.
# The target function hypothesis is visible to other objects via
# an accessor method.
#
####################################

class ExperimentGenerator:
    # Constructor for ExperimentGenerator 
    def __init__(self):
        self.initialBoard = [
        ["b", " ", "b", " ", "b" , " ", "b", " "],
        [" ", "b", " ", "b", " ", "b", " ", "b"],
        ["b", " ", "b", " ", "b" , " ", "b", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "r", " ", "r", " ", "r", " ", "r"],
        ["r", " ", "r", " ", "r" , " ", "r", " "],
        [" ", "r", " ", "r", " ", "r", " ", "r"],
        ]
    
    def getExperiment(self):
        return self.initialBoard