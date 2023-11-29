import argparse
import sys

def main(argv):
    parser = argparse.ArgumentParser(description="Drop sentence if it contains only unknown words",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--vocab", default='', type=str, help="Vocabulary", required=True)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    print("Read vocab from %s" % args.vocab, file=sys.stderr)
    words = set()
    with open(args.vocab, 'r') as vf:
        for line in vf:
            ws = line.split()
            if len(ws) > 0:
                words.add(ws[0])
    print("Read %d words" % len(words), file=sys.stderr)

    lc = 0
    sc = 0
    for line in sys.stdin:
        lc += 1
        line = line.strip()
        ws = line.split()
        ok = False
        for w in ws:
            if w in words:
                ok = True
                break
        if ok:
            print(line)
        else:
            # print(line, file=sys.stderr)
            sc += 1
    print("Wrote %d lines, %d skipped." % (lc, sc), file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
