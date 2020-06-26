import argparse
import data
import sys


def main(argv):
    parser = argparse.ArgumentParser(description="This script makes vocab from text file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--add-unk", default='', type=str, help="Unknown word to add if any")
    parser.add_argument("--add-eps", default='', type=str, help="Epsilon word to add if any")
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    words = set()
    lc = 0
    for line in sys.stdin:
        lc += 1
        ws = line.split()
        for w in ws:
            if w not in punctuation_vocabulary:
                words.add(w)
    print("Read %d lines, %d distinct words" % (lc, len(words)), file=sys.stderr)

    wc = 0
    if args.add_eps != '':
        print("Add aps: %s" % args.add_eps, file=sys.stderr)
        print("%s %d" % (args.add_eps, wc))
        wc += 1
    for w in sorted(words):
        print("%s %d" % (w, wc))
        wc += 1
    if args.add_unk != '' and args.add_unk not in words:
        print("Add unk: %s" % args.add_unk, file=sys.stderr)
        print("%s %d" % (args.add_unk, wc))
        wc += 1

    print("Wrote %d words" % wc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
