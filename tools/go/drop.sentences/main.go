
package main

import (
	"bitbucket.org/airenas/kirtis/tools/go/utils"
	"bufio"
	"flag"
	"io"
	"os"
	"strings"
	
	"github.com/pkg/errors"

	up "github.com/airenas/punctuator/tools/go/utils"

)

type lema interface {
	IsLt(w string) bool
	IsAbbreviation(w string) bool
	Close()
}

var lemaImpl lema

func init(){
	lemaImpl = up.NewLema()
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
		if isOK(line){
				os.Stdout.WriteString(line + "\n")
		}
	}
	lemaImpl.Close();
}

func isOK(line string) bool {
	if (line == ""){
		return false
	}
	lt, nlt := calc(line)
	if (nlt > 0){
		return false
	}
	if (lt == 0){
		return false
	}
	return true
}

func calc(line string) (int, int) {
	strs := strings.Split(line, " ")
	lt := 0
	nlt := 0
	for _, w := range strs{
		t := getType(w)
		if t == "lt" {
			lt ++;
		}
		if t == "nlt" {
			nlt ++;
			break
		}
	}
	return lt, nlt
}

func getType(w string) string{
	wc := up.GetWord(w)
	if (wc == "<NUM>"){
		return "num"
	}
	if wc == "" {
		if (isPunct(w)){
			return "punct"
		}
		return "empty"
	}
	if lemaImpl.IsLt(wc){
		return "lt"
	}
	if lemaImpl.IsAbbreviation(w){
		return "abrv"
	}
	return "nlt"
}

func isPunct(w string) bool {
	rs := []rune(w)
	if (len(rs) != 1){
		return false
	}
	_, ok := up.Punctuations[rs[0]]
	return ok
}
