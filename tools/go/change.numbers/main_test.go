package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNoChange(t *testing.T) {
	assert.Equal(t, "mama", changeLine("mama"))
	assert.Equal(t, "mama.", changeLine("mama."))
}

func TestChanges(t *testing.T) {
	assert.Equal(t, "mama <NUM>", changeLine("mama 10"))
	assert.Equal(t, "mama <NUM>", changeLine("mama 10,121"))
	assert.Equal(t, "mama <NUM>.", changeLine("mama 10."))
	assert.Equal(t, "mama <NUM>.<NUM>", changeLine("mama 10.121"))
	assert.Equal(t, "mama <NUM>-<NUM>", changeLine("mama 10-121"))
	assert.Equal(t, "mama <NUM>:<NUM>", changeLine("mama 10:10"))
	assert.Equal(t, "mama <NUM>/<NUM>", changeLine("mama 10/10"))
}
