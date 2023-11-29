import argparse
import sys

punct_dic = {',': ",COMMA", '.': ".PERIOD", '?': "?QUESTIONMARK", '!': "!EXCLAMATIONMARK", ':': ":COLON",
             ';': ";SEMICOLON",
             '-': "-DASH"}


def change_word(line):
    for c in line[1:]:
        r = punct_dic.get(c)
        if r is not None:
            return r
    return ""


def change_line(line):
    words = []
    wc = 0
    nc = 0
    for w in line.split():
        wc += 1
        if w[0] == '{':
            w = change_word(w)
            nc += 1
        if w != '':
            words.append(w)
    return ' '.join(words), wc, nc


def main(argv):
    parser = argparse.ArgumentParser(description="Fix spaces in input file",
                                     epilog="E.g. cat input.txt | " + sys.argv[0] + " > result.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args = parser.parse_args(args=argv)

    print("Starting", file=sys.stderr)

    lc = 0
    wc = 0
    pc = 0
    for line in sys.stdin:
        lc += 1
        line, wcl, pcl = change_line(line.strip())
        wc += wcl
        pc += pcl
        print(line)
    print("Read %d lines, %d words." % (lc, wc), file=sys.stderr)
    print("Changed %d puncts." % pc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
