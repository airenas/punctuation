import sys
from collections import namedtuple
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import data.data as data
import model.model as model

####################################################################################
Params = namedtuple('Params', ('vocab', 'trainData', 'validationData', 'hidden', 'wordVecSize',
                               'minibatches', 'modelFile', 'maxEpochs', 'gpu', 'callback', 'optimizer',
                               'features'),
                    defaults=(None, None, None, 100, 100, 128, None, 10, False, None, 'adam', None))


####################################################################################


def trainModel(params):
    if params.features is None:
        assert params.vocab, "No vocab provided"
    assert params.trainData, "No trainData"
    assert params.validationData, "No validationData"
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
    print("Train Data     :", params.trainData.len)
    print("Validation Data:", params.validationData.len)

    m = model.init(vocabularySize=v_size,
                   punctuationSize=len(data.PUNCTUATION_VOCABULARY),
                   hidden=params.hidden,
                   word_vector_size=params.wordVecSize,
                   optimizer=params.optimizer,
                   gpu=params.gpu, use_features=params.features is not None)
    m.summary(150)
    # keras.utils.plot_model(m, 'punc.png')
    # keras.utils.plot_model(m, 'punc_full.png', show_shapes=True)

    if params.features is None:
        gen_train = data.Generator(X=params.trainData.X, y=params.trainData.y, batch_size=params.minibatches)
        gen_valid = data.Generator(X=params.validationData.X, y=params.validationData.y, batch_size=params.minibatches)
    else:
        gen_train = data.FeaturesGenerator(m_data=params.trainData, features=params.features, batch_size=params.minibatches)
        gen_valid = data.FeaturesGenerator(m_data=params.validationData, features=params.features,
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
                           workers=8,
                           use_multiprocessing=True,
                           callbacks=callbacks
                           )
    # return m.fit(x = params.trainData.X, y = params.trainData.y,
    #                             validation_data=(params.validationData.X, params.validationData.y),
    #                             batch_size= params.minibatches,
    #                             epochs=params.maxEpochs,
    #                             verbose=1,
    #                             callbacks=callbacks
    #                             )
