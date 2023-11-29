import argparse
import sys

import ldata


def add(line):
    strs = line.split()
    if len(strs) < 1:
        return False
    w = strs[-1]
    if w == ldata.PunctS.period or w == ldata.PunctS.exclamation or w == ldata.PunctS.question or w == ldata.PunctS.semicolon:
        return False
    return True


def process(f_in, f_out):
    lc = 0
    dc = 0
    for line in f_in:
        lc += 1
        line = line.strip()
        if add(line):
            line = line + " " + ldata.PunctS.period
            dc += 1
        print(line, file=f_out)
    return lc, dc


def main(argv):
    parser = argparse.ArgumentParser(description="Add period at the end if there is none",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc, jc = process(sys.stdin, sys.stdout)
    print("Read %d lines." % lc, file=sys.stderr)
    print("Added %d periods." % jc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
