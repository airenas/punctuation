import argparse
import sys


def change_word(line):
    is_num = False
    for c in line:
        if c.isdigit():
            is_num = True
            continue
        if c == '.' or c == ',' or c == '/' or c == ':' or c == '-':
            continue
        return line
    if is_num:
        return '<NUM>'
    return line


def main(argv):
    parser = argparse.ArgumentParser(description="Fix spaces in input file",
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
            w = change_word(w)
            if w != '':
                words.append(w)
            if w == '<NUM>':
                nc += 1
        print(' '.join(words))
    print("Read %d lines, %d words" % (lc, wc), file=sys.stderr)
    print("Changed %d num." % nc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
