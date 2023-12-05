import argparse
import re
import sys

pattern = re.compile(r'<http(.+)>')


def change_line(line):
    res = re.sub(pattern, " [URL] ", line)
    res = res.replace("_", " ")
    return res.replace("<>", " ")

def main(argv):
    parser = argparse.ArgumentParser(description="Fix spaces in input file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc = 0
    for line in sys.stdin:
        lc += 1
        line = line.strip()
        print(change_line(line))
    print("Wrote %d lines." % lc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
