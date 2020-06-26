package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestEmpty(t *testing.T) {
	assert.Equal(t, "", change(""))
}

func TestNonePunct(t *testing.T) {
	assert.Equal(t, "mama mama", change("mama mama"))
}

func TestLDot(t *testing.T) {
	assert.Equal(t, "mama mama .PERIOD", change("mama mama."))
}

func TestInnerDot(t *testing.T) {
	assert.Equal(t, "mama. olia", change("mama. olia"))
}

func TestComma(t *testing.T) {
	assert.Equal(t, "mama ,COMMA <NUM> ?QUESTIONMARK", change("mama, <NUM>?"))
}

func TestSeveral(t *testing.T) {
	assert.Equal(t, "mama ,COMMA ?QUESTIONMARK .PERIOD", change("mama, ?."))
	assert.Equal(t, "mama ,COMMA -DASH ?QUESTIONMARK", change("mama,-?"))
}

func TestDotAlone(t *testing.T) {
	assert.Equal(t, "mama .PERIOD olia", change("mama . olia"))
}
