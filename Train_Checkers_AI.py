####################################
# File name: Train_Checkers_AI.py
# Author: BenjaminBeggs
# 
# Description: Master Python file that bridges data outputs between 
# the 4 Machine-Learning modules (PerformanceSystem, ExperimentGenerator,
# Critic, Generalizer) and manages the training process for the AI.
#
# Every 100th training experience will result in the recording of the
# of the updated target function approximation in a text file.
#
####################################

# Import pickle library to save target function approximations in text file
import pickle, symbol, logging, os, sys
sys.path.append(os.getcwd() + '/MachineLearningModules')

# Import machine-learning training modules
from ExperimentGenerator import ExperimentGenerator
from PerformanceSystem import PerformanceSystem
from Critic import Critic
from Generalizer import Generalizer

traceCount = pickle.load(open(os.getcwd() + "/SavedValues/traceCount.p", "rb"))
TRACEBACK_FILENAME = os.getcwd() + '/TraceBack/run' + str(traceCount) + '.out'
logging.basicConfig(filename=TRACEBACK_FILENAME, level=logging.DEBUG)

# Reroute system prints to a designated log file to retain past target function values
old_stdout = sys.stdout
log_file = open("targetHistory.log","w")
trace_log = open("gameTrace.log","w")

simCount = 0 # Counts simulations performed to know when to save the target function in a text file

# Read back Red hypothesis value from pickle file
currentHypothesisRed = pickle.load(open(os.getcwd() + "/SavedValues/targetHypothesisRed.p", "rb" ))
if (len(currentHypothesisRed) != 6):
    raise ValueError('There is something unusual about the dimensions of the Pickle file read for the Red hypothesis state. Please inspect it.')

# Read back Black hypothesis value from pickle file
currentHypothesisBlack = pickle.load(open(os.getcwd() + "/SavedValues/targetHypothesisBlack.p", "rb" ))
if (len(currentHypothesisBlack) != 6):
    raise ValueError('There is something unusual about the dimensions of the Pickle file read for the Black hypothesis state. Please inspect it.')

# Read back simulation magnitude value from pickle file
simMag = pickle.load(open(os.getcwd() + "/SavedValues/simMag.p", "rb"))

# Instantiate machine-learning objects
experGen = ExperimentGenerator()
perfSys = PerformanceSystem()
crit = Critic()
general = Generalizer()

# Print devnull logo along with current version of trained hypothesis coefficients
print(symbol.asci)
print("The most recent version of the Red train target function has weighting coefficients:", currentHypothesisRed)
print("The most recent version of the Black train target function has weighting coefficients:", currentHypothesisBlack)
print("This is the weighting coefficient generated by this number of simulations:", simMag*100)
input("Press Enter to initiate the learning process [learning process may be ended by pressing Ctrl-C]...")

# Continually run the machine-learning process to increase the accuracy of the target function approximation
try:
    while True:
        # Increment the simulation counter
        traceGenerated = 0
        simCount += 1
        
        # Retrieve a training experiment for the performance system
        trainingExperiment = experGen.getExperiment();

        # Call on the Performance System to generate a trace history
        # The trace generation is encapsulated in a try/catch block
        # in the case that a stale mate sequence or random range error
        # produces an incomplete trace history
        while traceGenerated != 1:
            try:
                sys.stdout = trace_log
                currentTrace = perfSys.getTrace(trainingExperiment, currentHypothesisRed, currentHypothesisBlack)
                traceGenerated = 1
                sys.stdout = old_stdout
            except Exception as e:
                sys.stdout = old_stdout
                logging.exception('Error detected.')
                print(e)
                print("An error was detected when performing trace generation. The traceback for this has been logged in /TraceBack/run" + str(traceCount) + ".log")
                traceCount += 1
                pickle.dump(traceCount, open(os.getcwd() + "/SavedValues/traceCount.p", "wb" ))
                TRACEBACK_FILENAME = os.getcwd() + '/TraceBack/run' + str(traceCount) + '.out'
                logging.basicConfig(filename=TRACEBACK_FILENAME, level=logging.DEBUG)
                input("Press enter to reexecute the trace generation, or Ctrl-C to exit the simulation.")

        # Generate training values using the trace history made by the performance system
        trainingValsRed = crit.generateTrainingValues(currentTrace[0], currentHypothesisRed)
        trainingValsBlack = crit.generateTrainingValues(currentTrace[1], currentHypothesisBlack)
        
        # Update the current hypothesis using the generalizer and training values
        currentHypothesisRed = general.updateHypothesis(trainingValsRed, currentHypothesisRed)
        currentHypothesisBlack = general.updateHypothesis(trainingValsBlack, currentHypothesisBlack)
        
        # 100 simulations have been performed, so the current hypothesis pickle file is updated
        # Additionally, the current hypothesis value is printed to the console and a log file for retention
        # A magnitude counter is incremented every 100 simulations to keep track of how many simulations
        # have been run since the initial arbitrary weighting values of [1, 1, 1, 1, 1, 1]
        if simCount == 100:
            simCount = 0
            simMag += 1
            print ("Simulation performed: ", (simMag*100))
            print ("Has produced Red hypothesis: ", currentHypothesisRed)
            print ("Has produced Black hypothesis: ", currentHypothesisBlack)
            # Reroute print to log file
            sys.stdout = log_file
            print ("Simulation performed: ", (simMag*100))
            print ("Has produced Red hypothesis: ", currentHypothesisRed)
            print ("Has produced Black hypothesis: ", currentHypothesisBlack)            # Reroute print back to console
            sys.stdout = old_stdout
            # Dump current hypothesis and simulation magnitude into pickle file for future recal
            pickle.dump(currentHypothesisRed, open(os.getcwd() + "/SavedValues/targetHypothesisRed.p", "wb" ))
            pickle.dump(currentHypothesisBlack, open(os.getcwd() + "/SavedValues/targetHypothesisBlack.p", "wb" ))
            pickle.dump(simMag, open(os.getcwd() + "/SavedValues/simMag.p", "wb" ))
# Watch for keyboard exceptions to allow user toggled simulation suspension
except KeyboardInterrupt:
    pass
    input("Training simulation ended by user.")