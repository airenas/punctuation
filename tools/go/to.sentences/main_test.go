package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestQuestionMark(t *testing.T) {
	test(t, "mama?\nolia", "mama? olia")
}

func TestExclamationMark(t *testing.T) {
	test(t, "mama!\nolia", "mama! olia")
}

func TestNone(t *testing.T) {
	test(t, "mama, olia", "mama, olia")
}

func TestDotNoSentence(t *testing.T) {
	test(t, "mama. olia", "mama. olia")
}

func TestDotProper(t *testing.T) {
	test(t, "m. Kauno", "m. Kauno")
}

func TestDotAbbeviation(t *testing.T) {
	test(t, "metai.\nKauno", "metai. Kauno")
}

func TestDotAbbeviation_NoSplit(t *testing.T) {
	test(t, "A. Antanas", "A. Antanas")
}

func TestDotAtEnd(t *testing.T) {
	test(t, "Metai.\nMetai.", "Metai. Metai.")
}

func TestNumLt(t *testing.T) {
	test(t, "tūkst. Lt", "tūkst. Lt")
}

func TestNumEur(t *testing.T) {
	test(t, "tūkst. Eur", "tūkst. Eur")
}

func test(t *testing.T, exp, line string) {
	l := splitIntoSentences(line)
	cmp := ""
	nl := ""
	for _, s := range l {
		cmp = cmp + nl + s
		nl = "\n"
	}
	assert.Equal(t, exp, cmp)
}
