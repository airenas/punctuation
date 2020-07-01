import argparse
import sys

import data


def main(argv):
    parser = argparse.ArgumentParser(description="This script makes training data from from text file. "
                                                 "Used for training with word features",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    lc = 0
    wc = 0
    pc = 0
    wl = 0
    num_total = 0
    current_words = []
    current_punctuations = []
    skip_until_eos = False
    last_token_was_punctuation = True
    last_eos_idx = 0
    for line in sys.stdin:
        lc += 1
        ws = line.split()
        for w in ws:
            if skip_until_eos:
                if w in data.EOS_TOKENS:
                    skip_until_eos = False
                continue
            elif w in punctuation_vocabulary:
                pc += 1
                if last_token_was_punctuation:  # hmm we need to solve this. how?....
                    # now if we encounter sequences like: "... !EXLAMATIONMARK .PERIOD ...", then we only use the
                    # first punctuation and skip the ones that follow
                    continue

                if w in data.EOS_TOKENS:
                    # no -1, because the token is not added yet
                    last_eos_idx = len(current_punctuations)
                punctuation = punctuation_vocabulary[w]
                current_punctuations.append(punctuation)
                last_token_was_punctuation = True
            else:
                wc += 1
                if not last_token_was_punctuation:
                    current_punctuations.append(punctuation_vocabulary[data.SPACE])
                current_words.append(w)
                last_token_was_punctuation = False
                num_total += 1

            if len(current_words) == data.MAX_SUBSEQUENCE_LEN:
                if last_eos_idx == 0:
                    skip_until_eos = True
                    current_words = []
                    current_punctuations = []
                    # next sequence starts with a new sentence, so is preceded by eos which is punctuation
                    last_token_was_punctuation = True
                else:
                    wl += 1
                    tw = current_words[:-1]
                    tw.append(data.END)
                    subsequence = [tw, current_punctuations]
                    print("%s" % repr(subsequence))
                    # Carry unfinished sentence to next subsequence
                    current_words = current_words[last_eos_idx + 1:]
                    current_punctuations = current_punctuations[last_eos_idx + 1:]
                    last_eos_idx = 0  # sequence always starts with a new sentence

    print("Read %d lines, Wrote %d batches" % (lc, wl), file=sys.stderr)
    print("Wrote %d words" % wc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
