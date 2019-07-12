import sys
import trainT

############ parameters
if len(sys.argv) > 1:
    dataDir = sys.argv[1]
else:
    sys.exit("Data dir argument missing")

if len(sys.argv) > 2:
    mPrefix = sys.argv[2]
else:
    sys.exit("Model file prefix argument missing")    

params = trainT.Params(
    vocab = dataDir + "/vocabulary",
    trainData = dataDir + "/train",
    validationData = dataDir + "/dev",
    modelFile = mPrefix + '_{epoch:02d}.h5',
    hidden = 512,
    gpu = True
)
############ training
trainT.trainModel(params)

print("Done")
