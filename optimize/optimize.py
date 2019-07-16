import sherpa
import callback
####################################################################################
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(parentdir, "tensorflow"))
import trainT
import data.data as data
####################################################################################
if len(sys.argv) > 1:
    dataDir = sys.argv[1]
else:
    sys.exit("Data dir argument missing")
####################################################################################
# hyper parameters
####################################################################################
minibatches=128
parameters = [sherpa.Discrete('num_units', [50, 512]),
              sherpa.Discrete('word_vec', [50, 512]),
              sherpa.Choice('optimizer', ["adam", "adagrad"])]

alg = sherpa.algorithms.RandomSearch(max_num_trials=30)
study = sherpa.Study(parameters=parameters,
                     algorithm=alg,
                     lower_is_better=True,
                     output_dir=".")
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
# optimize
####################################################################################
for trial in study:
    params = trainT.Params(
        vocab=vocab,
        trainData=trainData,
        validationData=validationData,
        modelFile='m_%s_%d_%d_{epoch:02d}.h5' % (
            trial.parameters["optimizer"], trial.parameters["word_vec"], trial.parameters["num_units"]),
        hidden=trial.parameters['num_units'],
        wordVecSize=trial.parameters['word_vec'],
        callback=callback.SherpaWrap(
            study.keras_callback(trial, objective_name='val_loss')),
        maxEpochs = 10,
        minibatches = minibatches,
        optimizer=trial.parameters["optimizer"],
        gpu=False
    )
    trainT.trainModel(params)

    #   callbacks=[study.keras_callback(trial, objective_name='loss')])
    study.finalize(trial)
    study.save()

####################################################################################
print(study.get_best_result())
study.save()
####################################################################################
