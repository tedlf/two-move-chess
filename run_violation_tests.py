from argparse import ArgumentParser
from glob import glob

import two_move_chess


def main(verbose):
    for violation_filename in sorted(glob('violations/*.pgn')):
        try:
            two_move_chess.main(violation_filename, [], None, False)
        except Exception as error:
            if verbose:
                print(violation_filename)
                print(error)
                print()
        else:
            raise Exception(f'The test in {violation_filename} did not elicit an exception')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
    args = parser.parse_args()

    main(args.verbose)
