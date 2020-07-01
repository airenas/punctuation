import numpy as np
import os
import sys
from collections import namedtuple
from tqdm import tqdm

from tensorflow import keras

####################################################################################
PUNCTUATION_VOCABULARY = ["_SPACE", ",COMMA", ".PERIOD", "?QUESTIONMARK", "!EXCLAMATIONMARK", ":COLON", ";SEMICOLON",
                          "-DASH"]
PUNCTUATION_MAPPING = {}
EOS_TOKENS = {".PERIOD", "?QUESTIONMARK", "!EXCLAMATIONMARK"}
END = "</S>"
UNK = "<UNK>"
SPACE = "_SPACE"
MAX_SUBSEQUENCE_LEN = 50
MAX_WORD_VOCABULARY_SIZE = 200000
####################################################################################

MData = namedtuple('MData', 'X, y, len')


def load(file):
    fs = os.stat(file).st_size
    resX = []
    resY = []
    with open(file, 'r') as f:
        with tqdm(total=fs, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for l in f:
                ld = eval(l)
                resX.append(ld[0])
                resY.append(keras.utils.to_categorical(ld[1], num_classes=len(PUNCTUATION_VOCABULARY)))
                pbar.update(len(l))
    return MData(X=np.array(resX).reshape(len(resX), len(resX[0])), y=np.array(resY), len=len(resX))


class Generator(keras.utils.Sequence):
    def __init__(self, X, y, batch_size):
        self.X = X
        self.y = y
        self.batch_size = batch_size

    def __len__(self):
        return int(np.floor(len(self.X) / self.batch_size))

    def __getitem__(self, batch_idx):
        X = self.X[batch_idx * self.batch_size:(batch_idx + 1) * self.batch_size]
        y = self.y[batch_idx * self.batch_size:(batch_idx + 1) * self.batch_size]
        # print("shapes x, y", X.shape, y.shape)
        return X, y

    def on_epoch_end(self):
        pass


def toDict(lines):
    return dict((x.strip(), i) for (i, x) in enumerate(lines))


def readVocabulary(file):
    with open(file, 'r', encoding='utf-8') as f:
        return toDict(f.readlines())


class FeaturesGenerator(keras.utils.Sequence):
    def __init__(self, m_data, features, batch_size):
        self.batch_size = batch_size
        self.m_data = m_data
        self.features = features

    def __len__(self):
        return int(np.floor(self.m_data.len / self.batch_size))

    def __getitem__(self, batch_idx):
        # print("Get %d." % batch_idx, file=sys.stderr)
        Xw = self.m_data.X[batch_idx * self.batch_size:(batch_idx + 1) * self.batch_size]
        y = self.m_data.y[batch_idx * self.batch_size:(batch_idx + 1) * self.batch_size]
        X = np.zeros(self.batch_size * self.features.len() * len(self.m_data.X[0]), dtype=np.float32).reshape((self.batch_size, len(self.m_data.X[0]), self.features.len()))
        for i in range(len(Xw)):
            for wi in range (len(Xw[i])):
                self.features.setWordFeaturesTo(Xw[i, wi], X[i, wi])
        # print("shapes x, y", X.shape, y.shape)
        return X, y

    def on_epoch_end(self):
        pass

    def count(self):
        return self.m_data.len
