# coding: utf-8
import model.model as model
import data.data as data
from tensorflow import keras
import numpy as np
import sys
import io 

MAX_SUBSEQUENCE_LEN = 50

def to_array(arr, dtype=np.int32):
    # minibatch of 1 sequence as column
    return np.array([arr], dtype=dtype).T

def convert_punctuation_to_readable(punct_token):
    if punct_token == data.SPACE:
        return " "
    else:
        return punct_token[0]

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben        

def restore(output_file, text, word_vocabulary, reverse_punctuation_vocabulary, predict_function):
    l = len(text)
    info = "Punctuating"
    i = 0
    progress(i, l, info)
    with open(output_file, 'w', encoding='utf-8') as f_out:
        while True:
            subsequence = text[i:i+MAX_SUBSEQUENCE_LEN]
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
                    last_eos_idx = len(punctuations) # we intentionally want the index of next element

            if subsequence[-1] == data.END:
                step = len(subsequence) - 1
            elif last_eos_idx != 0:
                step = last_eos_idx
            else:
                step = len(subsequence) - 1

            for j in range(step):
                f_out.write(" " + punctuations[j] + " " if punctuations[j] != data.SPACE else " ")
                if j < step - 1:
                    if subsequence[1+j] == data.END:
                        break    
                    f_out.write(subsequence[1+j])

            if subsequence[-1] == data.END:
                break

            i += step
            progress(i, l, info)

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

reverse_word_vocabulary = {v:k for k,v in vocab.items()}
reverse_punctuation_vocabulary = {v:k for k,v in punctuation_vocabulary.items()}

input_text = io.open(in_file, 'r', encoding='utf-8').read()

if len(input_text) == 0:
    sys.exit("Input text missing.")

text = [w for w in input_text.split() if w not in punctuation_vocabulary] + [data.END]

predict = lambda x : m.predict(x, verbose=0)

restore(output_file, text, vocab, reverse_punctuation_vocabulary, predict)

print("Done")