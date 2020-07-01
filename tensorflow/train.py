import sys
import trainT
import data.data as data
####################################################################################
minibatches=128
hidden=256
####################################################################################
############ parameters
####################################################################################
if len(sys.argv) > 1:
    dataDir = sys.argv[1]
else:
    sys.exit("Data dir argument missing")

if len(sys.argv) > 2:
    mPrefix = sys.argv[2]
else:
    sys.exit("Model file prefix argument missing")   
####################################################################################
# data
####################################################################################
print("Read vocabulary: ", dataDir + "/vocabulary")
vocab = data.readVocabulary(dataDir + "/vocabulary")  
####################################################################################

params = trainT.Params(
    vocab = vocab,
    trainFile = dataDir + "/train",
    validationFile = dataDir + "/train",
    modelFile = mPrefix + '_{epoch:02d}.h5',
    hidden = hidden,
    wordVecSize = hidden,
    minibatches = minibatches,
    gpu = False
)
############ training
trainT.trainModel(params)

print("Done")
