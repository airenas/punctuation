package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestEmpty(t *testing.T) {
	assert.Equal(t, "", change(""))
}

func TestLC(t *testing.T) {
	assert.Equal(t, "mama mama", change("mama mama"))
}

func TestLC1(t *testing.T) {
	assert.Equal(t, "mama mama.", change("mama Mama."))
}


func TestUC(t *testing.T) {
	assert.Equal(t, "mama Petras.", change("Mama Petras."))
}


func TestUC2(t *testing.T) {
	assert.Equal(t, "mama Petras.", change("MAMA PETRAS."))
}

func TestNum(t *testing.T) {
	assert.Equal(t, "mama <NUM>.", change("mama <NUM>."))
}
