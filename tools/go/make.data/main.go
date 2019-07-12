
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
}

func change(line string) string {
	strs := strings.Split(line, " ")
	res := ""
	a := ""
	for i, w := range strs{
		if (w != ""){
			res = res + a + changeWord(w, i == len(strs) - 1)
			a = " "
		}
	}
	return res
}

func changeWord(w string, last bool) string{
	rs := []rune (w)
	l := len(rs) - 1
	res := ""
	lr := rs[l]
	ch, ok := up.NNPunctuations[lr]
	if (ok && (lr != '.' || last)){
		if (l > 0){
			res = string(rs[0:l]) + " "
		}
		res = res + ch
	} else {
		res = w
	}
	return res
}
