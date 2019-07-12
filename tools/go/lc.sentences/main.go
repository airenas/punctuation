
package main

import (
	"unicode"
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
	IsProper(w string) bool
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
		line = change(line)
		os.Stdout.WriteString(line + "\n")
	}
	lemaImpl.Close();
}

func change(line string) string {
	strs := strings.Split(line, " ")
	res := ""
	a := ""
	for _, w := range strs{
		if (w != ""){
			res = res + a + changeWord(w)
			a = " "
		}
	}
	return res
}

func changeWord(w string) string{
	wc := up.GetWord(w)
	if (wc == "<NUM>"){
		return w
	}
	if (wc == ""){
		return w
	}
	if lemaImpl.IsProper(wc){
		return changeTitle(w)
	}
	return strings.ToLower(w)
}

func changeTitle(w string) string{
	r := []rune(strings.ToLower(w))
	r[0] = unicode.ToUpper(r[0])
	return string(r)
}
