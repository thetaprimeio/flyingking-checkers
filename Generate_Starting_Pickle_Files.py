####################################
# File name: Generate_Starting_Pickle_Files.py
# Author: BenjaminBeggs
# 
# Description: Encodes a set of starting Pickle bytefiles
# to initialize simulation count, Red target hypothesis,
# and Black target hypothesis.
#
# Also initializes a traceback error counter. 
#
####################################

import pickle, os

# Flag used to check for user input
inputFlag = False

while inputFlag != True:
    userIn = input("If you would like to reset the simulation Pickle files, please type YES (in all caps).")
    if userIn == "YES":
        startingMag = 0
        # Starting hypothesis arbitrarily set
        startingHypothesisRed = [-1, 1, -1, 1, 1, -1]
        startingHypothesisBlack = [1, -1, 1, -1, -1, 1]
        # Dump starting hypothesis to Pickle bytefiles
        pickle.dump(startingHypothesisRed, open(os.getcwd() + "/SavedValues/targetHypothesisRed.p", "wb" ))
        pickle.dump(startingHypothesisBlack, open(os.getcwd() + "/SavedValues/targetHypothesisBlack.p", "wb" ))
        pickle.dump(startingMag, open(os.getcwd() + "/SavedValues/simMag.p", "wb" ))
        pickle.dump(0, open(os.getcwd() + "/SavedValues/traceCount.p", "wb" ))
        inputFlag = True
        input("Pickle files for targetHypothesis[Red/Black] and simMag have been reset.")
        break
    # Catch unrecognized user input
    else:
        inputFlag = False
        print("Unrecognized input.")