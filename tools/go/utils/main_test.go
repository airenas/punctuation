package utils

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestWord(t *testing.T) {
	assert.Equal(t, "mama", GetWord("mama"))
}

func TestWordDot(t *testing.T) {
	assert.Equal(t, "mama", GetWord("mama,."))
}

func TestWordPunct(t *testing.T) {
	assert.Equal(t, "mama", GetWord("mama-"))
}

func TestWordNumber(t *testing.T) {
	assert.Equal(t, "mama10", GetWord("mama10-"))
}

