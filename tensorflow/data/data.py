from collections import namedtuple
from tensorflow import keras
import numpy as np

PUNCTUATION_VOCABULARY = ["_SPACE", ",COMMA", ".PERIOD", "?QUESTIONMARK", "!EXCLAMATIONMARK", ":COLON", ";SEMICOLON", "-DASH"]
PUNCTUATION_MAPPING = {}
EOS_TOKENS = {".PERIOD", "?QUESTIONMARK", "!EXCLAMATIONMARK"}
END = "</S>"
UNK = "<UNK>"
SPACE = "_SPACE"
MAX_SUBSEQUENCE_LEN = 50
MAX_WORD_VOCABULARY_SIZE=200000

MData = namedtuple('MData', 'X, y')

def load(file):
    resX = []
    resY = []
    with open(file, 'r') as f:
        for l in f:
            ld = eval(l)
            resX.append(ld[0])
            resY.append(keras.utils.to_categorical(ld[1], num_classes = len(PUNCTUATION_VOCABULARY)))
    return MData(X = np.array(resX).reshape(len(resX), len(resX[0])), y = np.array(resY))

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
