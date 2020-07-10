# coding: utf-8
import argparse
import io
import sys

import numpy as np
from tqdm import tqdm

import data.data as data
import model.model as model
from features import features

MAX_SUBSEQUENCE_LEN = 50


def to_array(arr, dtype=np.int32):
    # minibatch of 1 sequence as column
    return np.array([arr], dtype=dtype).T


def convert_punctuation_to_readable(punct_token):
    if punct_token == data.SPACE:
        return " "
    else:
        return punct_token[0]


def convert(words, features, word_function):
    res = np.zeros(features.len() * len(words), dtype=np.float32).reshape((len(words), features.len()))
    for i in range(len(words)):
        features.setWordFeaturesTo(word_function(words[i]), res[i])
    return res


def change_unk(w):
    if not (w.startswith("<") and w.endswith(">")):
        return w
    if w == '<NUM>' or w == data.END:
        return w
    return "<UNK>"


def restore(f_out, text, features, reverse_punctuation_vocabulary, predict_function, word_function):
    i = 0
    with tqdm(total=len(text), desc="Punctuating", file=sys.stderr) as pbar:
        while True:
            subsequence = text[i:i + MAX_SUBSEQUENCE_LEN]
            if len(subsequence) == 0:
                break
            if len(subsequence) < MAX_SUBSEQUENCE_LEN:
                subsequence = subsequence + ([data.END] * (MAX_SUBSEQUENCE_LEN - len(subsequence)))

            converted_subsequence = convert(subsequence, features, word_function)
            shape = converted_subsequence.shape
            a = np.array(converted_subsequence).reshape((1, shape[0], shape[1]))

            y = predict_function(a)

            f_out.write(subsequence[0])

            last_eos_idx = 0
            punctuations = []
            for y_t in y[0]:
                p_i = np.argmax(y_t.flatten())
                punctuation = reverse_punctuation_vocabulary[p_i]
                punctuations.append(punctuation)
                if punctuation in data.EOS_TOKENS:
                    last_eos_idx = len(punctuations)  # we intentionally want the index of next element

            if subsequence[-1] == data.END:
                step = len(subsequence) - 1
            elif last_eos_idx != 0:
                step = last_eos_idx
            else:
                step = len(subsequence) - 1

            for j in range(step):
                f_out.write(" " + punctuations[j] + " " if punctuations[j] != data.SPACE else " ")
                if j < step - 1:
                    if subsequence[1 + j] == data.END:
                        break
                    f_out.write(subsequence[1 + j])

            if subsequence[-1] == data.END:
                break

            i += step
            pbar.update(step)


############################################################################
def predict(args):
    print("Read Features from: ", args.features, file=sys.stderr)
    feat = features.Features(args.features)
    m = model.load(args.model)
    m.summary(150)
    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    reverse_punctuation_vocabulary = {v: k for k, v in punctuation_vocabulary.items()}
    print("Read test text: ", args.test, file=sys.stderr)
    input_text = io.open(args.test, 'r', encoding='utf-8').read()

    if len(input_text) == 0:
        sys.exit("Input text missing.")
    text = [w for w in input_text.split() if w not in punctuation_vocabulary] + [data.END]
    w_func = lambda x: x
    if args.change_unk:
        print("Change unk's", file=sys.stderr)
        w_func = lambda x: change_unk(x)
    predict_func = lambda x: m.predict(x, verbose=0)
    f_out = open(args.out, 'w', encoding='utf-8')
    print("Restoring punctuation", file=sys.stderr)
    restore(f_out, text, feat, reverse_punctuation_vocabulary, predict_func, w_func)


def take_cmd_params(argv):
    parser = argparse.ArgumentParser(
        description="This script predicts punctuation in text. Model must be trained with kaldi features",
        epilog="E.g. " + sys.argv[0] + "",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--test", default='', type=str, help="Test file", required=True)
    parser.add_argument("--out", default='', type=str, help="Output file", required=True)
    parser.add_argument("--features", default='', type=str, help="Features file", required=True)
    parser.add_argument("--change-unk", action='store_true', help="Change words like '<xxx>' to <UNK>")
    parser.add_argument("--model", default='', type=str, help="Model file", required=True)
    args = parser.parse_args(args=argv)
    return args


def main(argv):
    args = take_cmd_params(argv)
    print("Starting", file=sys.stderr)
    predict(args)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
