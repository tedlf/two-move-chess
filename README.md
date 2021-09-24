# Two Move Chess

This repository contains:
1. The [rules](http://htmlpreview.github.io/?https://github.com/tedlf/two-move-chess/blob/main/rules.html) of Two Move Chess, a chess variant designed to alleviate the first move advantage for White using double moves, while retaining the strategic and tactical play of international chess. These rules are also found on [chessvariants.com](https://www.chessvariants.com/invention/two-move-chess).
2. A Python module and scripts:
   1. The module two_move_chess.py extends the "Board" class of [python-chess](https://pypi.org/project/chess/). It can read and validate a modified PGN file that contains a game of Two Move Chess. It can also read a FEN file and display its board position. Board positions can be written to SVG files or as text to the terminal.
   2. Example PGN input files are in the "examples" directory, and the shell scripts example1.zsh, etc. contain examples of usage.
   3. The script "run_violation_tests.py" validates that files containing games that violate the rules of Two Move Chess (in the direcotry "violations") produce errors.
