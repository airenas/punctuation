package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNoChange(t *testing.T) {
	assert.Equal(t, "mama", changeLine("mama"))
}

func TestDrops(t *testing.T) {
	assert.Equal(t, "mama", changeLine("„mama”"))
}

func TestDropsDots(t *testing.T) {
	assert.Equal(t, "mama.", changeLine("mama..."))
	assert.Equal(t, "mama.", changeLine("mama.."))
}
