import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K


class Attention(layers.Layer):
    """
    Attention layer (https://arxiv.org/pdf/1409.0473.pdf).
    takes [encoder output, decoder output, encoder_last_state]
     """

    def __init__(self, **kwargs):
        super(Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        assert type(input_shape) == list
        enc_shape, dec_shape, _ = input_shape
        self.W_projected = self.add_weight(name='W_projected', shape=tf.TensorShape((enc_shape[2], enc_shape[2])),
                                           initializer='glorot_uniform', trainable=True)
        self.B_projected = self.add_weight(name='B_projected', shape=tf.TensorShape((1, enc_shape[2])),
                                           initializer='zeros', trainable=True)
        self.W_a = self.add_weight(name='W_a', shape=tf.TensorShape((dec_shape[2], enc_shape[2])),
                                   initializer='glorot_uniform', trainable=True)
        self.V_a = self.add_weight(name='V_a', shape=tf.TensorShape((enc_shape[2], 1)),
                                   initializer='glorot_uniform', trainable=True)

        super(Attention, self).build(input_shape)

    def call(self, inputs):
        """
        inputs: [encoder_output_sequence, decoder_output_sequence, encoder_last_state]
        """
        assert type(inputs) == list
        encoder_out_seq, decoder_out_seq, initState = inputs

        projected_context = K.dot(encoder_out_seq, self.W_projected) + self.B_projected

        dec_hidden = decoder_out_seq.shape[2]
        timesteps = encoder_out_seq.shape[1]

        def step(inputs, states):
            state = states[0]
            ha = K.expand_dims(K.dot(state, self.W_a), 1)
            e = K.tanh(projected_context + ha)
            alphas = K.exp(K.dot(e, self.V_a))
            alphas = K.reshape(alphas, (-1, timesteps))
            alphas = alphas / (K.sum(alphas, axis=1, keepdims=True) + K.epsilon())
            weighted_context = encoder_out_seq * alphas[:, :, None]
            weighted_context = K.sum(weighted_context, axis=1)
            return weighted_context, [inputs]
        # initState = K.zeros_like(projected_context[:, 1, 0:dec_hidden])
        _, wc, _ = K.rnn(step, decoder_out_seq, [initState])
        return wc

    def compute_output_shape(self, input_shape):
        enc_shape, _, _ = input_shape
        return [enc_shape]
