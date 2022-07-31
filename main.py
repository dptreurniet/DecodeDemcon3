import sys
from solver import Solver
import mineField

"""
Main file for Demcon Decode Challenge nr. 3: Minesweeper Solver

Author: Daan Treurniet
Date: 31-07-2022
"""

if __name__ == "__main__":

    config = mineField.BEGINNER_FIELD
    args = sys.argv[1:]

    valid_args_message = 'Invalid argument.\n' \
                         'Valid arguments are:' \
                         '[\"beginner\"; \"intermediate\"; \"expert\"; width: int, height: int, number_of_mines: int]'

    # Interpret input arguments
    if len(args) == 1:
        if args[0] == 'beginner':
            config = mineField.BEGINNER_FIELD
        elif args[0] == 'intermediate':
            config = mineField.INTERMEDIATE_FIELD
        elif args[0] == 'expert':
            config = mineField.EXPERT_FIELD
        else:
            print(valid_args_message)
            sys.exit()

    if len(args) == 3:
        try:
            width = int(args[0])
            height = int(args[1])
            n_mines = int(args[2])
            config = {'width': width, 'height': height, 'number_of_mines': n_mines}
        except ValueError:
            print(valid_args_message)
            sys.exit()

    # Initialize solver and run it
    try:
        solver = Solver(config)
    except TypeError as e:
        print(e)
        sys.exit()
    except ValueError as e:
        print(e)
        sys.exit()

    mines = solver.run()

    # Output mine coordinates
    if len(mines) > 0:
        print('\nMine coordinates:')
        print('\n'.join("(%s, %s)" % coord for coord in mines))
    else:
        print('\nNo mines found...')
