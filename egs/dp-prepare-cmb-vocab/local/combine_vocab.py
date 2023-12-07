import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description="This script makes vocab of n items reading from stdin",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--n", default='', type=int, help="Vocab size")
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    words = set()
    wc = 0
    for line in sys.stdin:
        w = line.strip()
        if w not in words:
            wc += 1
            words.add(w)
            print(f"{w}")
            if args.n <= wc:
                break
    print("Wrote %d words" % wc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
