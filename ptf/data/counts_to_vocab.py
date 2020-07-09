import argparse
import sys


def is_ok(w, args):
    if args.drop_unk and w.startswith("<") and w.endswith(">") and not (w in args.leave):
        return False
    return True


def main(argv):
    parser = argparse.ArgumentParser(description="Makes vocab from counts file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--n", default=0, type=int, help="Take n first words")
    parser.add_argument("--drop_unk", action='store_true', help="Skip words like '<xxx>'")
    parser.add_argument("--leave", type=str, help="Leave unknown word. Sample --leave '<unk>'", action='append')
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)
    print("Leave", args.leave, file=sys.stderr)
    lc = 0
    n = 0
    for line in sys.stdin:
        lc += 1
        ws = line.split()
        if len(ws[0]) > 0 and is_ok(ws[0], args):
            print(ws[0])
            n += 1
        if args.n > 0 and n >= args.n:
            break

    print("Read %d lines" % lc, file=sys.stderr)
    print("Wrote %d words" % n, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
