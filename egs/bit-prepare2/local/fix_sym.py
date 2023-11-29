import argparse
import sys

change_dict = {'–': '-'}


def change_line(line):
    res = []
    for c in line:
        v = change_dict.get(c)
        if v is not None:
            c = v
        res.append(c)
    return ''.join(res)


def main(argv):
    parser = argparse.ArgumentParser(description="Fix spaces in input file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc = 0
    sc = 0
    for line in sys.stdin:
        lc += 1
        line = line.strip()
        print(change_line(line))
    print("Wrote %d lines." % lc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
