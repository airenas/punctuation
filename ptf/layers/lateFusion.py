import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K


class LateFusion(layers.Layer):
    """LateFusion layer.
    """

    def __init__(self, **kwargs):
        super(LateFusion, self).__init__(**kwargs)

    def build(self, input_shape):
        assert type(input_shape) == list
        gru_shape, context_shape = input_shape
        self.W_context = self.add_weight('W_context', shape=tf.TensorShape((context_shape[2], gru_shape[2])),
                                         initializer='zeros', trainable=True)
        self.W_context2 = self.add_weight('W_context2', shape=tf.TensorShape((gru_shape[2], gru_shape[2])),
                                          initializer='zeros', trainable=True)
        self.W_gru = self.add_weight('W_gru', shape=tf.TensorShape((gru_shape[2], gru_shape[2])),
                                     initializer='zeros', trainable=True)
        self.B = self.add_weight('B', shape=tf.TensorShape((1, gru_shape[2])),
                                 initializer='zeros', trainable=True)
                                 
        super(LateFusion, self).build(input_shape)                          

    def call(self, inputs):
        # takes [encoder_output, context]
        assert type(inputs) == list
        gru, context = inputs
        lfc = K.dot(context, self.W_context)
        fw = K.dot(lfc, self.W_context2) + K.dot(gru, self.W_gru) + self.B
        fws = keras.activations.sigmoid(fw)
        res = lfc * fws + gru
        return res

    def compute_output_shape(self, input_shape):
        assert type(input_shape) == list
        gru_shape, _ = input_shape
        return [gru_shape]
