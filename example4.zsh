#!/bin/zsh

# This script takes an output directory for SVG files as an argument. If the argument
# is not supplied, text output is printed to the screen.

if [ -z "$1" ]; then
    python two_move_chess.py -f examples/example4.fen
else
    mkdir -p "$1"
    python two_move_chess.py -f examples/example4.fen -o end:"$1"/example4.svg
fi
