"""
This Python module extends the |Board| class of the python-chess module
(https://pypi.org/project/chess/) to conform to the rules of Two Move Chess
(https://www.chessvariants.com/invention/two-move-chess).

When run as a script, this module reads and validates a modified PGN file that
contains a game of Two Move Chess. It can also read a FEN file and display
its board position. Board positions can be written to SVG files or as text
to the terminal.

Example input files are in the "examples" directory, and the shell scripts
example1.zsh, etc. in this directory contain examples of usage.

The directory "violations" contains examples of games that violate the rules
of Two Move Chess. The script "run_violation_tests.py" validates that those
files produce errors.

"""

import re
from argparse import ArgumentParser
from enum import Enum

import chess
import chess.svg

EXPECTED_RESULTS = ['1/2-1/2', '1-0', '0-1', '*']

KINGSIDE_CASTLING = 'O-O'
QUEENSIDE_CASTLING = 'O-O-O'
CASTLING = KINGSIDE_CASTLING, QUEENSIDE_CASTLING
ROOK_CASTLES_TO = {
    chess.WHITE: {
        KINGSIDE_CASTLING: 5,
        QUEENSIDE_CASTLING: 3,
    },
    chess.BLACK: {
        KINGSIDE_CASTLING: 61,
        QUEENSIDE_CASTLING: 59,
    },
}


class MoveType(Enum):
    START_OF_GAME = 0
    DOUBLE_MOVE_HALF = 1
    DOUBLE_MOVE = 2
    SINGLE_MOVE = 3
    RESPONSE_MOVE = 4


HTML_STYLE = {
    MoveType.DOUBLE_MOVE: ('', ''),
    MoveType.SINGLE_MOVE: ('<strong>', '</strong>'),
    MoveType.RESPONSE_MOVE: ('<em><strong>', '</strong></em>'),
}


class TwoMoveChessBoard(chess.Board):
    """
    This class extends |chess.Board| for the purpose of verifying games of Two Move Chess.
    """

    def __init__(self, fen=None, debug=False, print_unicode=False, html_output=False):
        if fen is None:
            super().__init__()
            self.last_move_type = MoveType.START_OF_GAME
        else:
            super().__init__(fen)
            self.last_move_type = MoveType.DOUBLE_MOVE
        self.piece_count = []
        self.debug = debug
        self.print_unicode = print_unicode
        self.html_output = html_output

    def push_san(self, move, move_type):
        super().push_san(move)
        self.piece_count.append(len(self.piece_map()))
        self.last_move_type = move_type

    def double_move_turn(self, turn):
        move1, move2 = turn.split(',')
        rook_castling_square = ROOK_CASTLES_TO[self.turn][move1] if move1 in CASTLING else None
        self.push_san(move1, MoveType.DOUBLE_MOVE_HALF)
        if self.last_move_valid_single():
            raise Exception(f'This is not a valid two move turn: {turn}')
        self.turn = not self.turn
        self.push_san(move2, MoveType.DOUBLE_MOVE)
        if self.move_stack[-1].from_square in (self.move_stack[-2].to_square, rook_castling_square):
            raise Exception(f'The same piece cannot move twice in one turn: {turn}')

    def single_move_turn(self, turn):
        self.push_san(turn, MoveType.SINGLE_MOVE)
        if not self.last_move_valid_single():
            raise Exception(f'This cannot be a single move turn: {turn}')

    def response_move_turn(self, turn):
        self.push_san(turn, MoveType.RESPONSE_MOVE)

    def last_move_valid_single(self):
        """
        Determine if the last move met any of the criteria for a single move turn:
            1. The move placed the opponent in check (or checkmate)
            2. The move provided an opportunity for an en passant capture
            3. The move captured an opponent's piece
            4. The move promoted a pawn
        """
        if self.is_check() or self.is_checkmate():
            return True
        elif self.has_legal_en_passant():
            return True
        elif self.piece_count[-1] != self.piece_count[-2]:
            return True
        elif self.move_stack[-1].promotion is not None:
            return True
        return False

    def play(self, turns):
        """
        Play the sequence of |turns|. An exception will be thrown if any turn
        is not a legal Two Move Chess turn.
        """
        html_turn_data = []
        for player_turn in turns:
            if self.last_move_type in (MoveType.DOUBLE_MOVE, MoveType.RESPONSE_MOVE):
                if ',' in player_turn:
                    self.double_move_turn(player_turn)
                else:
                    self.single_move_turn(player_turn)
            elif self.last_move_type in (MoveType.START_OF_GAME, MoveType.SINGLE_MOVE):
                if ',' not in player_turn:
                    self.response_move_turn(player_turn)
                else:
                    raise Exception(f'Illegal player turn {player_turn} following {self.last_move_type}')
            else:
                raise Exception(f'Illegal last move type: {self.last_move_type}')
            if self.debug:
                print(f'{player_turn.ljust(9)}\t{self.last_move_type}', end='\t')
                if self.turn:  # Black
                    print()
            elif self.html_output:
                if not self.turn:  # White
                    html_turn_data.append([(player_turn, self.last_move_type)])
                else:  # Black
                    html_turn_data[-1].append((player_turn, self.last_move_type))
        if self.html_output:
            print('\n'.join(html_table(html_turn_data)))

    def is_repetition(self):
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')

    def can_claim_threefold_repetition(self):
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')

    def is_fivefold_repetition(self):
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')

    def can_claim_fifty_moves(self):
        """ This method will be replaced by |can_claim_fifty_turns| in Two Move Chess. """
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')

    def is_fifty_moves(self):
        """ This method will be replaced by |is_fifty_turns| in Two Move Chess. """
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')

    def is_seventyfive_moves(self):
        """ This method will be replaced by |is_seventyfive_turns| in Two Move Chess. """
        raise NotImplementedError('This method has not been implemented yet for Two Move Chess')


def html_table(html_turn_data):
    """ Produce an HTML table for the current game in a format appropriate for chessvariants.com. """
    table = ['<table border="0" cellpadding="1" cellspacing="1" style="width:75px">', '  <tbody>']
    for turn_number, turn in enumerate(html_turn_data):
        table.extend(table_row(turn_number, turn))
    table.extend(('  </tbody>', '</table>'))
    return table


def table_row(turn_number, turn):
    """ Produce a row for the HTML table created by |html_table| for a single full turn. """
    style = HTML_STYLE[turn[0][1]]
    row = ['    <tr>', f'      <td>{turn_number + 1}.{style[0]}{turn[0][0]}{style[1]}', '      </td>']
    if len(turn) == 2:
        style = HTML_STYLE[turn[1][1]]
        row.append(f'      <td>{style[0]}{turn[1][0]}{style[1]}')
    else:
        row.append('      <td>&nbsp;')
    row.extend(('      </td>', '    </tr>'))
    return row


def read_pgn(input_filename):
    """
    Read a PGN file for a game of Two Move Chess. The file format is nearly the
    same as that of a PGN file for international chess. The moves of a two move turn
    are separated by a comma.
    """
    turn_pattern = re.compile(r'\d+\.(.*)')
    with open(input_filename) as input_file:
        game = []
        for line in input_file:
            turn_match = turn_pattern.match(line)
            if turn_match is not None:
                game.extend(m.split('.')[1] if '.' in m else m for m in turn_match.group(1).split())
    if game[-1] in EXPECTED_RESULTS:
        game.pop()
    return game


def print_board(board, output_filename=None):
    if output_filename is not None:
        with open(output_filename, 'w') as svg_file:
            svg_file.write(chess.svg.board(board, size=400))
        print(f'Output file: {output_filename}')
    elif not board.html_output:
        if board.debug and not board.turn:
            print()
        if board.print_unicode:
            # Print a unicode board
            print(board.unicode(invert_color=True, empty_square='.'))
        else:
            # Print an ASCII board
            print(board)
        print()


def process_output_actions(raw_output_actions, max_section_end=0):
    """
    Output actions are from the -o command line option. Actions that contain a colon
    are expected to contain a turn number and an output file name. For example, the
    action "8:images/example5a.svg" will produce the file "example5a.svg" after turn 8.
    An action that has "end" instead of a turn number will produce the file at the end
    of the game, for example "end:images/example5c.svg".

    Actions without a colon are expected to contain a turn number. The board position
    will be printed to the screen after that turn. The board position at the end of the
    game will always be printed to the screen if not specified to be printed to a file.

    Turn numbers can contain a half-turn, for example 8.5. Turn numbers are doubled to
    become a "player turn count". Turn numbers that are beyond the end of the game are
    ignored.

    Example 5 (from example5.zsh):
    >>> print(process_output_actions(['8', '20'], 62))
    [(16, None), (40, None), (62, None)]

    Example 5 (from example5.zsh with argument "images"):
    >>> print(process_output_actions(['8:images/example5a.svg', '20:images/example5b.svg', 'end:images/example5c.svg'], 62))
    [(16, 'images/example5a.svg'), (40, 'images/example5b.svg'), (62, 'images/example5c.svg')]

    """

    output_actions = []
    end_found = False
    for action in raw_output_actions:
        turn_number, filename = action.split(':') if ':' in action else (action, None)
        if turn_number == 'end':
            player_turn_number = max_section_end
            end_found = True
        else:
            player_turn_number = int(2 * float(turn_number))
            if player_turn_number == max_section_end:
                end_found = True
        if player_turn_number <= max_section_end:
            output_actions.append((player_turn_number, filename))
    if not end_found:
        output_actions.append((max_section_end, None))
    return output_actions


def main(input_filename, raw_output_actions, debug, print_unicode, html_output):
    if input_filename.endswith('.pgn'):
        board = TwoMoveChessBoard(None, debug, print_unicode, html_output)
        player_turns = read_pgn(input_filename)
        output_actions = process_output_actions(raw_output_actions, len(player_turns) + 1)
        section_start = 0
        for section_end, output_filename in sorted(output_actions, key=lambda x: x[0]):
            board.play(player_turns[section_start:section_end])
            print_board(board, output_filename)
            section_start = section_end
    elif input_filename.endswith('.fen'):
        with open(input_filename) as input_file:
            fen = input_file.readline()
        board = TwoMoveChessBoard(fen, print_unicode=print_unicode)
        output_actions = process_output_actions(raw_output_actions)
        print_board(board, output_actions[0][1])
    else:
        raise Exception(f'Input file name does not end in ".pgn" or ".fen": {input_filename}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='Input PGN or FEN file')
    parser.add_argument(
        '-o', '--output', default=[], action='append', help='output turn number, OR output turn number:output filename'
    )
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    parser.add_argument('-u', '--unicode', action='store_true', help='Use unicode when printing board to screen')
    parser.add_argument('--html', action='store_true', help='Print game in an HTML table')
    args = parser.parse_args()

    main(args.file, args.output, args.debug, args.unicode, args.html)
