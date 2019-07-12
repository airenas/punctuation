package utils

var Punctuations map[rune]bool

func init() {
	Punctuations = make(map[rune]bool)
	for _, r := range ",.!?-:;" {
		Punctuations[r] = true
	}
}

func GetWord(w string) string {
	rs := []rune(w)
	l := len(rs)
	for ; l > 0 && isPunct(rs[l-1]); l-- {
	}
	return string(rs[0:l])
}

func isPunct(r rune) bool {
	_, ok := Punctuations[r]
	return ok
}

var NNPunctuations = map[rune]string{
	'.': ".PERIOD",
	'?': "?QUESTIONMARK",
	'!': "!EXCLAMATIONMARK",
	',': ",COMMA",
	';': ";SEMICOLON",
	':': ":COLON",
	'-': "-DASH",
}
