# coding: utf-8
import sys

import numpy as np
from tqdm import tqdm

import data.data as data
import model.model as model

MAX_SUBSEQUENCE_LEN = 50


def to_array(arr, dtype=np.int32):
    # minibatch of 1 sequence as column
    return np.array([arr], dtype=dtype).T


def convert_punctuation_to_readable(punct_token):
    if punct_token == data.SPACE:
        return " "
    else:
        return punct_token[0]


def restore(output_file, text_iter, word_vocabulary, reverse_punctuation_vocabulary, predict_function, total_words):
    info = "Punctuating"

    progress_bar = tqdm(desc="Processing", unit=" words", total=total_words)

    def fill_text(text):
        for item in text_iter:
            text.append(item)
            progress_bar.update(1)
            if len(text) >= MAX_SUBSEQUENCE_LEN:
                break
        return text

    i = 0
    text = []
    with open(output_file, 'w', encoding='utf-8') as f_out:
        while True:
            text = fill_text(text[i:]).copy()
            subsequence = text
            if len(subsequence) == 0:
                break
            if len(subsequence) < MAX_SUBSEQUENCE_LEN:
                subsequence = subsequence + ([data.END] * (MAX_SUBSEQUENCE_LEN - len(subsequence)))

            converted_subsequence = [word_vocabulary.get(w, word_vocabulary[data.UNK]) for w in subsequence]

            a = np.array(converted_subsequence).reshape(1, len(converted_subsequence))

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

            i = step

        progress_bar.close()


def word_iterator(file_path, punctuation_vocabulary):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            for w in words:
                if w not in punctuation_vocabulary:
                    yield w
    yield data.END


def calc_words(iter_w):
    res = 0
    for w in iter_w:
        res += 1
    return res


############################################################################
if len(sys.argv) > 1:
    in_file = sys.argv[1]
else:
    sys.exit("Input file path argument missing")

if len(sys.argv) > 2:
    vocab_file = sys.argv[2]
else:
    sys.exit("Vocab file path argument missing")

if len(sys.argv) > 3:
    m_file = sys.argv[3]
else:
    sys.exit("Model file path argument missing")

if len(sys.argv) > 4:
    output_file = sys.argv[4]
else:
    sys.exit("Output file path argument missing")
############################################################################

print('Loading vocab')
vocab = data.readVocabulary(vocab_file)
print('Loading model')
m = model.load(m_file)
m.summary(150)

punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)

reverse_word_vocabulary = {v: k for k, v in vocab.items()}
reverse_punctuation_vocabulary = {v: k for k, v in punctuation_vocabulary.items()}

predict = lambda x: m.predict(x, verbose=0)

total = calc_words(word_iterator(in_file, punctuation_vocabulary))
print(f'Test words {total}')

restore(output_file, word_iterator(in_file, punctuation_vocabulary), vocab, reverse_punctuation_vocabulary, predict,
        total)

print("Done")
