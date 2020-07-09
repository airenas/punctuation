import argparse
import sys


def change_line(line):
    res = []
    pr = ' '
    pc = 0
    for c in line:
        if c == '{':
            pc += 1
        if c == '}':
            pc -= 1
        assert pc < 2, "Double {!"
        assert pc >= 0, "Double }!"
        if c == '{' and pr != ' ':
            res.append(' ')
        if pr == '}' and c != ' ':
            res.append(' ')
        if not (c == ' ' and pc > 0):
            res.append(c)
        pr = c
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
