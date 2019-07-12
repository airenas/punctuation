package utils

import (
	"golang.org/x/text/encoding/charmap"
	"unicode"
	"time"
	"sync"
	"github.com/pkg/errors"
	"io"
	"bufio"
	"path"
	"os"
	"strings"
	"bitbucket.org/airenas/kirtis/tools/go/utils/lema"
)

type lInfo struct {
	abbreviation bool
	proper       bool
	lt           bool
	number       bool
}

//Lema helper class
type Lema struct {
	words map[string]*lInfo
	path  string
	m sync.Mutex
	save bool
	vFileName string
}

func (l * Lema) IsAbbreviation(w string) bool {
	if strings.HasSuffix(w, ".") && strings.Title(w) == w && len(w) == 2 {
		return true
	}
	r := l.getData(w)
	return r.abbreviation
}

func (l * Lema) IsProper(w string) bool {
	r := l.getData(w)
	return r.proper
}

func (l * Lema) IsLt(w string) bool {
	r := l.getData(w)
	return r.lt
}

func NewLema() *Lema {
	l := Lema{}
	l.vFileName = l.vocabFile()
	l.loadMap()
	go l.runSave()
	return &l
}


func (l * Lema) getData(w string) *lInfo {
	l.m.Lock()
	defer l.m.Unlock()

	r, ok := l.words[w]
	if (ok){
		return r
	}
	r = l.getDataFromServer(w)
	l.words[w] = r
	l.save = true
	return r
}

func (l * Lema) getDataFromServer(w string) *lInfo {
	var res lInfo
	if (unicode.IsLetter([]rune(w)[0]) && !hasNonLT(w) && !hasHTTPSymbols(w)){
		r, err := lema.Analyze(w)
		
		if (err != nil){
			panic(errors.Wrap(err, "Can't analyze '" + w + "'"))
		}
		res.proper = isProper(r)
		res.lt = isLt(r)
		res.abbreviation = isAbbreviation(r)
	}
	
	return &res
}

func (l * Lema) vocabFile() string {
	home, err := os.UserHomeDir()
	if (err != nil){
		panic (err)
	}
	dir := path.Join(home, ".punct", "cache", "vocab")
	return dir
}


func (l * Lema) loadMap() {
	l.m.Lock()
	defer l.m.Unlock()

	l.words = make (map[string]*lInfo)
	_, err := os.Stat(l.vFileName)
    if os.IsNotExist(err) {
        return 
	}
	l.loadVocab(l.vFileName)
}

func (l * Lema) Close() {
	l.saveVocab()		
}

func (l * Lema) runSave() {
	for {
		time.Sleep(30*time.Second)
		l.saveVocab()		
	}
}
func (l * Lema) saveVocab() {
	l.m.Lock()
	defer l.m.Unlock()
	if (!l.save){
		return
	}
	file, err := os.OpenFile(l.vFileName, os.O_WRONLY|os.O_TRUNC|os.O_CREATE, 0644)
    if err != nil {
        panic(err)
    }
    defer file.Close()
     
    for k, v := range l.words { 
		file.Write([]byte(k + " " + toStr(v) + "\n"))
	}
}

func toStr(l* lInfo) string {
	res := "w"
	if (l.proper) {
		res = res + "P"
	}
	if (l.abbreviation) {
		res = res + "A"
	}
	if (l.lt) {
		res = res + "L"
	}
	if (l.number) {
		res = res + "N"
	}
	return res
}

func (l * Lema) loadVocab(f string) {
	file, err := os.Open(f)
	if err != nil {
		panic(err)
	}
	
	rd := bufio.NewReader(file)

	for {
		line, err := rd.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			panic(errors.Wrap(err, "Read file line error"))
		}
		strs := strings.Split(line, " ")
		li := lInfo{}
		li.proper = strings.Index(strs[1], "P") > -1
		li.abbreviation = strings.Index(strs[1], "A") > -1
		li.lt = strings.Index(strs[1], "L") > -1
		li.number = strings.Index(strs[1], "N") > -1
		l.words[strs[0]] = &li		
	}
}

func isProper(r *lema.Result) bool {
	if r.Suffix != "" { // ignore our suffix check
		return false
	}
	for _, mi := range r.Mi {
		if !strings.HasPrefix(mi.Mi, "I") {
			return false
		}
	}
	return len(r.Mi) > 0
}

func isAbbreviation(r *lema.Result) bool {
	if r.Suffix != "" { // ignore our suffix check
		return false
	}
	for _, mi := range r.Mi {
		if !strings.HasPrefix(mi.MiVdu, "Y") {
			return false
		}
	}
	return len(r.Mi) > 0
}

func isLt(r *lema.Result) bool {
	if r.Suffix != "" { // ignore our suffix check
		return false
	}
	return len(r.Mi) > 0
}

var encoder = charmap.ISO8859_13.NewEncoder()

func hasNonLT(w string) bool {
	_, err := encoder.String(w)
	return err != nil
}

func hasHTTPSymbols(w string) bool {
	return strings.Index(w, "/") > 0 || strings.Index(w, "%") > 0 || strings.Index(w, ">") > 0
}
