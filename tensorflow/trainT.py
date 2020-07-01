import sys
from collections import namedtuple
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import data.data as data
import model.model as model

####################################################################################
Params = namedtuple('Params', ('vocab', 'trainFile', 'validationFile', 'hidden', 'wordVecSize',
                               'minibatches', 'modelFile', 'maxEpochs', 'gpu', 'callback', 'optimizer',
                               'features'),
                    defaults=(None, None, None, 100, 100, 128, None, 10, False, None, 'adam', None))


####################################################################################


def trainModel(params):
    if params.features is None:
        assert params.vocab, "No vocab provided"
    assert params.trainFile, "No trainFile"
    assert params.validationFile, "No validationFile"
    assert params.modelFile, "No modelFile provided"

    if params.features is None:
        print("Vocab size     :", len(params.vocab))
        v_size = len(params.vocab)
    else:
        print("Features count :", params.features.len())
        v_size = params.features.len()
    print("Hidden layer   :", params.hidden)
    print("Word vec size  :", params.wordVecSize)
    print("Use GPU        :", params.gpu)
    print("Minibatches    :", params.minibatches)
    print("Models out dir :", params.modelFile)
    if params.features is None:
        print("Train Data     :", len(params.trainData.X))
        print("Validation Data:", len(params.validationData.X))

    m = model.init(vocabularySize=v_size,
                   punctuationSize=len(data.PUNCTUATION_VOCABULARY),
                   hidden=params.hidden,
                   word_vector_size=params.wordVecSize,
                   optimizer=params.optimizer,
                   gpu=params.gpu, use_features=params.features is not None)
    m.summary(150)
    # keras.utils.plot_model(m, 'punc.png')
    # keras.utils.plot_model(m, 'punc_full.png', show_shapes=True)

    print("Loading train data: ", params.trainFile, file=sys.stderr)
    train_data = data.load(params.trainFile)
    print("Train data len = ", train_data.len, file=sys.stderr)

    print("Loading validation data: ", params.validationFile, file=sys.stderr)
    validation_data = data.load(params.validationFile)
    print("Validation data len = ", validation_data.len, file=sys.stderr)

    if params.features is None:
        gen_train = data.Generator(X=train_data.X, y=train_data.y, batch_size=params.minibatches)
        gen_valid = data.Generator(X=validation_data.X, y=validation_data.y, batch_size=params.minibatches)
    else:
        gen_train = data.FeaturesGenerator(m_data=train_data, features=params.features, batch_size=params.minibatches)
        gen_valid = data.FeaturesGenerator(m_data=validation_data, features=params.features,
                                           batch_size=params.minibatches)

    print("Training", file=sys.stderr)

    checkpoint = ModelCheckpoint(filepath=params.modelFile,
                                 monitor='loss',
                                 verbose=1,
                                 save_best_only=False,
                                 mode='min',
                                 period=1)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
    callbacks = [checkpoint, es]
    if params.callback is not None:
        callbacks.insert(0, params.callback)

    return m.fit_generator(generator=gen_train,
                           validation_data=gen_valid,
                           epochs=params.maxEpochs,
                           verbose=1,
                           # workers=1,
                           # use_multiprocessing=False,
                           callbacks=callbacks
                           )
    # return m.fit(x = params.trainData.X, y = params.trainData.y,
    #                             validation_data=(params.validationData.X, params.validationData.y),
    #                             batch_size= params.minibatches,
    #                             epochs=params.maxEpochs,
    #                             verbose=1,
    #                             callbacks=callbacks
    #                             )
