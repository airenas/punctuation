import argparse
import sys

import data


def read_vocab(file_path):
    result_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            key = line.strip()
            result_dict[key] = True
    return result_dict


def main(argv):
    parser = argparse.ArgumentParser(description="This script calculate unk word in text text file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + "",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--vocab", default='', type=str, help="Vocabulary")
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    print(f'Read vocab {args.vocab}', file=sys.stderr)
    vocab = read_vocab(args.vocab)
    print(f'Read vocab {len(vocab)}, punct {len(punctuation_vocabulary)}', file=sys.stderr)

    wc, pc, uc = 0, 0, 0
    for line in sys.stdin:
        ws = line.split()
        for w in ws:
            wc += 1
            if w in punctuation_vocabulary:
                pc += 1
            if w not in vocab:
                uc += 1
    print(f'Read {wc - pc} words, unk {uc}, punct {pc}', file=sys.stderr)
    if wc > pc:
        print(f'OOV {uc / (wc - pc)}', file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
