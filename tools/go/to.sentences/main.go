
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
	IsAbbreviation(w string) bool
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
		l := splitIntoSentences(line)
		for _, s := range l {
			if line != "" {
				os.Stdout.WriteString(s + "\n")
			}
		}
	}
	lemaImpl.Close();
}

func splitIntoSentences(line string) []string {
	var r []string
	strs := strings.Split(line, " ")
	if len(strs) == 0 {
		return r
	}
	sent := ""
	a := ""
	for i, s := range strs {
		sent = sent + a + s
		if isSentenceEnd(strs, i){
			r = append(r, strings.TrimSpace(sent))
			sent = ""
			a = ""
		}
		a = " "
	}
	if (sent != ""){
		r = append(r, strings.TrimSpace(sent))
	}
	return r
}

func isSentenceEnd(strs []string, pos int) bool {
	s := strs[pos]
	if strings.HasSuffix(s, "?") || strings.HasSuffix(s, "!"){
		return true
	}
	if strings.HasSuffix(s, ".") && isDotSentenceEnd(strs, pos){
		return true		
	}

	return false
}

func isDotSentenceEnd(strs []string, pos int) bool {
	s := strs[pos]
	next := ""
	if (pos + 1 < len(strs)){
		next = strs[pos + 1]
	}
	if (strings.Title(next) != next) {
		return false
	}
	if isProper(next) && isAbbreviation(s){
		return false
	}
	if isCurrency(next) && isAbbreviation(s) {
		return false
	}
	return true
}

func isProper(w string) bool {
	wc := up.GetWord(w)
	if wc == "" {
		return false
	}
	return lemaImpl.IsProper(wc)
}

func isCurrency(w string) bool {
	wc := up.GetWord(w)
	return wc == "Lt" || wc == "Cnt" || wc == "Eur" 
}

func isAbbreviation(s string) bool {
	return lemaImpl.IsAbbreviation(s)
}

