# coding: utf-8
from __future__ import division, print_function

import random
import os
import sys
import operator
try:
    import cPickle
except ImportError:
    import _pickle as cPickle
try:
    input = raw_input
except NameError:
    pass
from io import open
import fnmatch
import shutil

parentdir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0,parentdir)
import data.data as dt

# path to text file in the format:
# word1 0.123 0.123 ... 0.123
# word2 0.123 0.123 ... 0.123 etc...
# e.g. glove.6B.50d.txt
PRETRAINED_EMBEDDINGS_PATH = None

MIN_WORD_COUNT_IN_VOCAB = 2

PUNCTUATION_MAPPING = {}

# punctuations that are not included in vocabulary nor mapping, must be added to CRAP_TOKENS
CRAP_TOKENS = {"<doc>", "<doc.>"}
PAUSE_PREFIX = "<sil="

# replacement for pickling that takes less RAM. Useful for large datasets.


def dump(d, path):
    with open(path, 'w') as f:
        for s in d:
            f.write("%s\n" % repr(s))


def load(path):
    d = []
    with open(path, 'r') as f:
        for l in f:
            d.append(eval(l))
    return d


def add_counts(word_counts, line):
    for w in line.split():
        if w in CRAP_TOKENS or w in dt.PUNCTUATION_VOCABULARY or w in PUNCTUATION_MAPPING or w.startswith(PAUSE_PREFIX):
            continue
        word_counts[w] = word_counts.get(w, 0) + 1


def build_vocabulary(word_counts):
    # Unk will be appended to end
    return [wc[0] for wc in reversed(sorted(word_counts.items(), key=operator.itemgetter(1))) if wc[1] >= MIN_WORD_COUNT_IN_VOCAB and wc[0] != dt.UNK][:dt.MAX_WORD_VOCABULARY_SIZE]


def write_vocabulary(vocabulary, file_name):
    if dt.END not in vocabulary:
        vocabulary.append(dt.END)
    if dt.UNK not in vocabulary:
        vocabulary.append(dt.UNK)

    print("Vocabulary size: %d" % len(vocabulary))

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(vocabulary))


def iterable_to_dict(arr):
    return dict((x.strip(), i) for (i, x) in enumerate(arr))


def read_vocabulary(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return iterable_to_dict(f.readlines())


def write_processed_dataset(input_files, output_file, vocab_file):
    """
    data will consist of two sets of aligned subsequences (words and punctuations) of MAX_SEQUENCE_LEN tokens (actually punctuation sequence will be 1 element shorter).
    If a sentence is cut, then it will be added to next subsequence entirely (words before the cut belong to both sequences)
    """

    data = []

    word_vocabulary = read_vocabulary(vocab_file)
    punctuation_vocabulary = iterable_to_dict(dt.PUNCTUATION_VOCABULARY)

    num_total = 0
    num_unks = 0

    current_words = []
    current_punctuations = []
    current_pauses = []

    # if it's still 0 when MAX_SEQUENCE_LEN is reached, then the sentence is too long and skipped.
    last_eos_idx = 0
    last_token_was_punctuation = True  # skipt first token if it's punctuation
    last_pause = 0.0

    # if a sentence does not fit into subsequence, then we need to skip tokens until we find a new sentence
    skip_until_eos = False

    for input_file in input_files:

        with open(input_file, 'r', encoding='utf-8') as text:

            for line in text:

                for token in line.split():

                    # First map oov punctuations to known punctuations
                    if token in PUNCTUATION_MAPPING:
                        token = PUNCTUATION_MAPPING[token]

                    if skip_until_eos:

                        if token in dt.EOS_TOKENS:
                            skip_until_eos = False

                        continue

                    elif token in CRAP_TOKENS:
                        continue

                    elif token.startswith(PAUSE_PREFIX):
                        last_pause = float(token.replace(
                            PAUSE_PREFIX, "").replace(">", ""))

                    elif token in punctuation_vocabulary:

                        if last_token_was_punctuation:  # if we encounter sequences like: "... !EXLAMATIONMARK .PERIOD ...", then we only use the first punctuation and skip the ones that follow
                            continue

                        if token in dt.EOS_TOKENS:
                            # no -1, because the token is not added yet
                            last_eos_idx = len(current_punctuations)

                        punctuation = punctuation_vocabulary[token]

                        current_punctuations.append(punctuation)
                        last_token_was_punctuation = True

                    else:

                        if not last_token_was_punctuation:
                            current_punctuations.append(
                                punctuation_vocabulary[dt.SPACE])

                        word = word_vocabulary.get(token, word_vocabulary[dt.UNK])

                        current_words.append(word)
                        current_pauses.append(last_pause)
                        last_token_was_punctuation = False

                        num_total += 1
                        num_unks += int(word == word_vocabulary[dt.UNK])

                    # this also means, that last token was a word
                    if len(current_words) == dt.MAX_SUBSEQUENCE_LEN:

                        assert len(current_words) == len(
                            current_punctuations) + 1, "#words: %d; #punctuations: %d" % (len(current_words), len(current_punctuations))
                        assert current_pauses == [] or len(current_words) == len(
                            current_pauses), "#words: %d; #pauses: %d" % (len(current_words), len(current_pauses))

                        # Sentence did not fit into subsequence - skip it
                        if last_eos_idx == 0:
                            skip_until_eos = True

                            current_words = []
                            current_punctuations = []
                            current_pauses = []

                            # next sequence starts with a new sentence, so is preceded by eos which is punctuation
                            last_token_was_punctuation = True

                        else:
                            subsequence = [
                                current_words[:-1] + [word_vocabulary[dt.END]],
                                current_punctuations,
                                current_pauses[1:]
                            ]

                            data.append(subsequence)

                            # Carry unfinished sentence to next subsequence
                            current_words = current_words[last_eos_idx+1:]
                            current_punctuations = current_punctuations[last_eos_idx+1:]
                            current_pauses = current_pauses[last_eos_idx+1:]

                        last_eos_idx = 0  # sequence always starts with a new sentence

    print("%.2f%% UNK-s in %s" % (num_unks / num_total * 100, output_file))

    dump(data, output_file)


def create_dev_test_train_split_and_vocabulary(root_path, create_vocabulary, train_output, dev_output, test_output, pretrained_embeddings_path=None, vocab_file=None):

    train_txt_files = []
    dev_txt_files = []
    test_txt_files = []

    if create_vocabulary and not pretrained_embeddings_path:
        word_counts = dict()

    for root, dirnames, filenames in os.walk(root_path):
        for filename in fnmatch.filter(filenames, '*.txt'):

            path = os.path.join(root, filename)

            if filename.endswith(".test.txt"):
                test_txt_files.append(path)

            elif filename.endswith(".dev.txt"):
                dev_txt_files.append(path)

            else:
                train_txt_files.append(path)

                if create_vocabulary and not pretrained_embeddings_path:
                    with open(path, 'r', encoding='utf-8') as text:
                        for line in text:
                            add_counts(word_counts, line)

    if create_vocabulary:
        if pretrained_embeddings_path:
            vocabulary = []
            embeddings = []
            with open(pretrained_embeddings_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.split()
                    w = line[0]
                    e = [float(x) for x in line[1:]]
                    vocabulary.append(w)
                    embeddings.append(e)

            with open("We.pcl", 'wb') as f:
                cPickle.dump(embeddings, f, cPickle.HIGHEST_PROTOCOL)
        else:
            vocabulary = build_vocabulary(word_counts)
        write_vocabulary(vocabulary, vocab_file)

    write_processed_dataset(train_txt_files, train_output, vocab_file)
    write_processed_dataset(dev_txt_files, dev_output, vocab_file)
    write_processed_dataset(test_txt_files, test_output, vocab_file)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        sys.exit("The path to stage1 source data directory with txt files is missing")

    if len(sys.argv) > 2:
        data_path = sys.argv[2]
    else:
        sys.exit("The path to output data directory is missing")

    TRAIN_FILE = os.path.join(data_path, "train")
    DEV_FILE = os.path.join(data_path, "dev")
    TEST_FILE = os.path.join(data_path, "test")

    # Stage 2
    TRAIN_FILE2 = os.path.join(data_path, "train2")
    DEV_FILE2 = os.path.join(data_path, "dev2")
    TEST_FILE2 = os.path.join(data_path, "test2")

    WORD_VOCAB_FILE = os.path.join(data_path, "vocabulary")

    replace = False
    if os.path.exists(data_path):

        while True:
            resp = input(
                "Data path '%s' already exists. Do you want to:\n[r]eplace the files in existing data path?\n[e]xit?\n>" % data_path)
            resp = resp.lower().strip()
            if resp not in ('r', 'e'):
                continue
            if resp == 'e':
                sys.exit()
            elif resp == 'r':
                replace = True
            break

    if replace and os.path.exists(data_path):
        shutil.rmtree(data_path)

    os.makedirs(data_path)

    create_dev_test_train_split_and_vocabulary(
        path, True, TRAIN_FILE, DEV_FILE, TEST_FILE, PRETRAINED_EMBEDDINGS_PATH, WORD_VOCAB_FILE)

    # Stage 2
    if len(sys.argv) > 3:
        path2 = sys.argv[3]
        create_dev_test_train_split_and_vocabulary(
            path2, False, TRAIN_FILE2, DEV_FILE2, TEST_FILE2)
