
package main

import (
	"bufio"
	"flag"
	"io"
	"os"
	"strings"
	"unicode"

	"github.com/pkg/errors"

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
	strs := strings.Split(line, " ")
	if len(strs) == 0 {
		return line
	}
	res := make([]string, 0)
	for _, s := range strs {
		res = append(res, changeWord(s))
	}
	return strings.Join(res, " ")
}

func isNum(w string) bool {
	runes := []rune(w)
	if len(runes) == 0 {
		return false
	}
	for _, r := range runes {
		if !(uint32(r) == ',' || unicode.IsDigit(r)) {
			return false
		}
	}
	return true
}

func changeWord(w string) string {
	for _, s := range ".-:/" {
		w = trySplitWith(w, s)
	}
	return w
}

func trySplitWith(w string, c rune) string {
	strs := strings.Split(w, string(c))
	if len(strs) == 0 {
		return w
	}
	r := ""
	a := ""
	for _, s := range strs {
		if (isNum(s)){
			r = r + a + "<NUM>"
		} else {
			r = r + a + s
		}
		a = string(c)
	}
	return r
}
