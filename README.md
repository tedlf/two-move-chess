# Two Move Chess

This repository contains:
1. The [rules](http://htmlpreview.github.io/?https://github.com/tedlf/two-move-chess/blob/main/rules.html) of Two Move Chess, a chess variant designed to alleviate the first move advantage for White using double moves, while retaining the strategic and tactical play of international chess. These rules are also found on [chessvariants.com](https://www.chessvariants.com/invention/two-move-chess).
2. The Python module [two_move_chess.py](two_move_chess.py), which extends the <strong>Board</strong> class of [python-chess](https://pypi.org/project/chess/). It can read and validate a modified PGN file that contains a game of Two Move Chess. It can also read a FEN file and display its board position. Board positions can be written to SVG files or as text to the terminal.
3. The [examples](examples) directory contains PGN files for the examples used in the [rules](http://htmlpreview.github.io/?https://github.com/tedlf/two-move-chess/blob/main/rules.html). These shell scripts validate the examples, and illustrate the use of [two_move_chess.py](two_move_chess.py):
   * [example1.zsh](example1.zsh)
   * [example2.zsh](example2.zsh)
   * [example3.zsh](example3.zsh)
   * [example4.zsh](example4.zsh)
   * [example5.zsh](example5.zsh)
4. The script [run_violation_tests.py](run_violation_tests.py) validates that errors are produced by games that violate the [rules](http://htmlpreview.github.io/?https://github.com/tedlf/two-move-chess/blob/main/rules.html) of Two Move Chess. The incorrect games are in the [violations](violations) directory.
