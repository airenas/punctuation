import data
import sys


def main(argv):
    print("Starting", file=sys.stderr)
    punctuation_vocabulary = data.toDict(data.PUNCTUATION_VOCABULARY)
    words = dict()
    lc = 0
    for line in sys.stdin:
        lc += 1
        ws = line.split()
        for w in ws:
            if w not in punctuation_vocabulary:
                if w in words:
                    words[w] = words[w] + 1
                else:
                    words[w] = 1
    print("Read %d lines, %d distinct words" % (lc, len(words)), file=sys.stderr)

    words_sorted = sorted(words.items(), key=lambda x: x[0])

    wc = 0
    for w in words_sorted:
        print("%s %d" % (w[0], w[1]))
        wc += 1
    print("Wrote %d words" % wc, file=sys.stderr)
    print("Done", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
