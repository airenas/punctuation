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

print("Loading train data: ", dataDir + "/train")
trainData = data.load(dataDir + "/train")
print("Train data len = ", len(trainData.X))

print("Loading validation data: ", dataDir + "/dev")
validationData = data.load(dataDir + "/dev")
print("Validation data len = ", len(validationData.X))
####################################################################################     

params = trainT.Params(
    vocab = vocab,
    trainData = trainData,
    validationData = validationData,
    modelFile = mPrefix + '_{epoch:02d}.h5',
    hidden = hidden,
    wordVecSize = hidden,
    minibatches = minibatches,
    gpu = False
)
############ training
trainT.trainModel(params)

print("Done")
