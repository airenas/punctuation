import argparse
import sys

import ldata


def line_ok(line):
    strs = line.split()
    for w in strs[:-1]:
        if w == ldata.PunctS.period or w == ldata.PunctS.exclamation or w == ldata.PunctS.question:
            return False
    return True


def process(f_in, f_out):
    lc = 0
    dc = 0
    for line in f_in:
        lc += 1
        line = line.strip()
        if line_ok(line):
            print(line, file=f_out)
        else:
            # print(line, file=sys.stderr)
            dc += 1
    return lc, dc


def main(argv):
    parser = argparse.ArgumentParser(description="Drop sentences if it contains sentence end in the middle of the line",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc, jc = process(sys.stdin, sys.stdout)
    print("Read %d lines." % lc, file=sys.stderr)
    print("Dropped %d sentences." % jc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
