import data
import sys


def main(argv):
    print("Starting", file=sys.stderr)
    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    lc = 0
    pc = 0
    for line in sys.stdin:
        lc += 1
        ws = line.split()
        for w in ws:
            if w not in punctuation_vocabulary:
                print("%s" % w, end=" ")
            else:
                pc += 1
        print("")

    print("Read %d lines, dropped %d puncts" % (lc, pc), file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
