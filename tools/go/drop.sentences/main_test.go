package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestEmpty(t *testing.T) {
	assert.False(t, isOK(""))
}

func TestEmpty2(t *testing.T) {
	assert.False(t, isOK("."))
}

func TestNum(t *testing.T) {
	assert.False(t, isOK("<NUM>"))
}

func TestNum2(t *testing.T) {
	assert.False(t, isOK("<NUM>, <NUM>"))
}


func TestOK(t *testing.T) {
	assert.True(t, isOK("Valio."))
}


func TestNonLt(t *testing.T) {
	assert.False(t, isOK("Valio zxcxzc."))
}

func TestAbbreviations(t *testing.T) {
	assert.True(t, isOK("Mama D."))
}
