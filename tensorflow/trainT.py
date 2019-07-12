import model.model as model
import data.data as data
from tensorflow import keras
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from collections import namedtuple

Params = namedtuple('Params', ('vocab', 'trainData', 'validationData', 'hidden', 'minibatches', 'modelFile', 'maxEpochs', 'gpu'),
                    defaults=(None, None, None, 100, 128, None, 10, False))


def trainModel(params):
    assert params.vocab, "No vocab provided"
    assert params.trainData, "No trainData"
    assert params.validationData, "No validationData"
    assert params.modelFile, "No modelFile provided"
    
    print("Read vocabulary: ", params.vocab)
    vocab = data.readVocabulary(params.vocab)
    print("Vocab size:", len(vocab))
    print("Hidden layer:", params.hidden)
    print("Use GPU:", params.gpu)
    print("Minibatches:", params.minibatches)
    print("Train Data:", params.trainData)
    print("Validation Data:", params.validationData)

    m = model.init(vocabularySize=len(vocab),
                   punctuationSize=len(data.PUNCTUATION_VOCABULARY),
                   hidden=params.hidden,
                   word_vector_size=params.hidden,
                   gpu=params.gpu)
    m.summary(150)
    # keras.utils.plot_model(m, 'punc.png')
    # keras.utils.plot_model(m, 'punc_full.png', show_shapes=True)

    print("Loading train data: ", params.trainData)
    train_data = data.load(params.trainData)
    print("Train data len = ", len(train_data.X))
    gen_train = data.Generator(
        X=train_data.X, y=train_data.y, batch_size=params.minibatches)

    print("Loading validation data: ", params.validationData)
    validation_data = data.load(params.validationData)
    print("Validation data len = ", len(validation_data.X))
    gen_valid = data.Generator(
        X=validation_data.X, y=validation_data.y, batch_size=params.minibatches)

    print("Training")

    checkpoint = ModelCheckpoint(params.modelFile,
                                 monitor='loss',
                                 verbose=1,
                                 save_best_only=False,
                                 mode='min',
                                 period=1)
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)

    return m.fit_generator(generator=gen_train,
                           validation_data=gen_valid,
                           epochs=params.maxEpochs,
                           verbose=1,
                           workers=8,
                           use_multiprocessing=True,
                           callbacks=[es, checkpoint]
                           )
