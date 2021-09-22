#!/bin/zsh

# This script takes an output directory for SVG files as an argument. If the argument
# is not supplied, text output is printed to the screen.

if [ -z "$1" ]; then
    python two_move_chess.py -f examples/example5.pgn -o 8 -o 20
else
    mkdir -p "$1"
    python two_move_chess.py -f examples/example5.pgn -o 8:"$1"/example5a.svg -o 20:"$1"/example5b.svg -o end:"$1"/example5c.svg
fi
