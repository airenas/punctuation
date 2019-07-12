package main

import (
	"github.com/pkg/errors"
	"io"
	"bufio"
	"flag"
	"os"
	"strings"

	"bitbucket.org/airenas/kirtis/tools/go/utils"
)

func main() {
	filePtr := flag.String("f", "", "file")
	flag.Parse()

	r, err := utils.NewReader(*filePtr)
	if err != nil {
		panic(err)
	}
	defer r.Close()

	rd := bufio.NewReader(r.Reader)

	for {
		line, err := rd.ReadString('\n')
        if err != nil {
            if err == io.EOF {
                break
            }
            panic(errors.Wrap(err, "Read file line error"))
		}
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "//") {
			os.Stdout.WriteString(line + "\n")
		} else {
			l := changeLine(line)
			os.Stdout.WriteString(l + "\n")
		}
	}
}

func changeLine(line string) string {
	i := strings.Index(line, " ")
	if (i > 0) {
		return line[i + 1: ]
	}
	return line
}