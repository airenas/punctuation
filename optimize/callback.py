import tensorflow as tf
import datetime


class SherpaWrap(tf.keras.callbacks.Callback):
    def __init__(self, sherpaCallback):
        self.sherpaCallback = sherpaCallback

    def on_epoch_end(self, epoch, logs=None):
        self.sherpaCallback.on_epoch_end(epoch, logs)
