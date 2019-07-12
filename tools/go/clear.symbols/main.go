package main

import (
	"bufio"
	"flag"
	"io"
	"os"
	"strings"

	"github.com/pkg/errors"

	"bitbucket.org/airenas/kirtis/tools/go/utils"
)

var replaceableSyblols map[rune]rune

func init() {
	replaceableSyblols = make(map[rune]rune)
	for _, r := range []rune("()\"`<>“”„“„” '*") {
		replaceableSyblols[r] = ' '
	}
	replaceableSyblols['–'] = '-'
}

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
	if len(line) == 0 {
		return line
	}
	runes := []rune(line)
	res := make([]rune, 0)
	for _, r := range runes {
		res = append(res, changeSymbol(r))
	}
	r := string(res)
	r = strings.TrimSpace(r)
	r = strings.ReplaceAll(r, "  ", " ")
	r = strings.ReplaceAll(r, "...", ".")
	r = strings.ReplaceAll(r, "..", ".")
	return string(r)
}

func changeSymbol(r rune) rune {
	s, ok := replaceableSyblols[r]
	if (ok){
		return s
	}
	return r
}
