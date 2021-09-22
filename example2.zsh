#!/bin/zsh

# This script takes an output directory for SVG files as an argument. If the argument
# is not supplied, the only output is text printed to the screen.

if [ -z "$1" ]; then
    python two_move_chess.py -f examples/example2.pgn
else
    mkdir -p "$1"
    python two_move_chess.py -f examples/example2.pgn -o end:"$1"/example2.svg
fi
