import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import layers.attention as la
import layers.lateFusion as llf


def init(vocabularySize=1, punctuationSize=1, timesteps=50, word_vector_size=100, hidden=100, gpu=False,
         optimizer='adam', use_features=False):
    # input
    if not use_features:
        word_ids = keras.Input(shape=(timesteps,), dtype='int32', name='word_ids')
        word_vec = layers.Embedding(output_dim=word_vector_size, input_dim=vocabularySize, input_length=1,
                                    name='word_vec')(word_ids)
    else:
        word_ids = keras.Input(shape=(timesteps, vocabularySize,), dtype='float32', name='feat_ids')
        word_vec = layers.Dense(word_vector_size, input_dim=vocabularySize, name='feat_matrix', use_bias=True,
                                activation=tf.nn.tanh)(word_ids)
    # encoder layer
    gru_input, f_state, b_state = layers.Bidirectional(__createGRULayer(hidden, True, 'gru_input'))(word_vec)

    # decoder
    gru_output = __createGRULayer(hidden, False, 'gru')([gru_input, b_state])

    attention_output = la.Attention(name='attention_layer')([gru_input, gru_output, b_state])
    lf_output = llf.LateFusion(name='late_fusion')([gru_output, attention_output])

    # output
    out = layers.Dense(punctuationSize, name='out')(lf_output)
    out = layers.TimeDistributed(layers.Softmax())(out)
    # ignore first value as we do not predict for the first word
    out = layers.Lambda(lambda x: x[:, 1:])(out)

    # model
    model = keras.Model(inputs=word_ids, outputs=out, name='punctuation')
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    return model


def load(file):
    return keras.models.load_model(file, custom_objects={'LateFusion': llf.LateFusion,
                                                         'Attention': la.Attention})


def __createGRULayer(hidden, returnState, lName):
    return layers.GRU(hidden, return_sequences=True, return_state=returnState, name=lName)
