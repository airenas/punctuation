import argparse
import sys

import ldata


def process(f_in, f_out):
    lc = 0
    jc = 0
    join = False
    sep = ''
    for line in f_in:
        lc += 1
        line = line.strip()
        strs = line.split()
        if len(strs) > 0:
            p = strs[len(strs) - 1]
            if p == ldata.PunctS.colon:
                join = True
            elif join and (p == ldata.PunctS.semicolon or p == ldata.PunctS.comma):
                join = True
            else:
                join = False
        if join:
            print(sep + line, end="", file=f_out)
            sep = ' '
            jc += 1
        else:
            print(sep + line, file=f_out)
            sep = ''
    if join:
        print('', file=f_out)
    return lc, jc


def main(argv):
    parser = argparse.ArgumentParser(description="Fix spaces in input file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc, jc = process(sys.stdin, sys.stdout)
    print("Read %d lines." % lc, file=sys.stderr)
    print("Joined %d sentences." % jc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
