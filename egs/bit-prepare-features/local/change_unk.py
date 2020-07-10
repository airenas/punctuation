import argparse
import sys


def change_word(w):
    if not (w.startswith("<") and w.endswith(">")):
        return w, 0
    if w == "<NUM>":
        return w, 0
    return "<UNK>", 1


def main(argv):
    parser = argparse.ArgumentParser(description="Changes everything in <xxx> to <UNK>",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc = 0
    nc = 0
    wc = 0
    for line in sys.stdin:
        lc += 1
        line = line.strip()
        words = []
        for w in line.split():
            wc += 1
            w, c = change_word(w)
            if w != '':
                words.append(w)
            nc += c
        print(' '.join(words))

    print("Read %d lines, %d words" % (lc, wc), file=sys.stderr)
    print("Changed %d unk." % nc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
