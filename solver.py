import mineField
from enum import Enum
from random import sample


class GameOver(Exception):
    pass


class CellState(Enum):
    UNKNOWN = 0
    SAFE = 1
    MINE = 2


class Solver:
    """Minefield solver class"""
    def __init__(self, configuration: dict):
        self.minefield = mineField.MineField(**configuration)
        self.width = configuration['width']
        self.height = configuration['height']

        # 2D arrays to keep track of cell states and number of adjacent mines for safe cells
        self.states = [[CellState.UNKNOWN for _ in range(self.width)] for __ in range(self.height)]
        self.adj_mines = [[-1 for _ in range(self.width)] for __ in range(self.height)]

    def __print(self) -> None:
        """
        Convenience function to print field to output.
        :return: None
        """
        print('')
        for row in range(self.height):
            for col in range(self.width):
                state = self.states[row][col]
                c = ''
                if state == CellState.UNKNOWN:
                    c = '_'
                if state == CellState.MINE:
                    c = 'x'
                if state == CellState.SAFE:
                    c = self.adj_mines[row][col]

                print(' ' + str(c) + ' ', end='')
            print('')

    def __get_neighbours(self, col: int, row: int) -> list:
        """
        Function that returns the list of neighbouring cells.
        :param col: Column index of cell.
        :param row: Row index of cell.
        :return: List of neighbouring cells as tuples (col, row)
        """
        neighbours = []
        for row_offset in [-1, 0, 1]:
            for col_offset in [-1, 0, 1]:
                # Skip this iteration if both offsets are 0 or one of them is out of range
                if row_offset == col_offset == 0:
                    continue
                if 0 <= row+row_offset < self.height and 0 <= col+col_offset < self.width:
                    neighbours.append((col+col_offset, row+row_offset))
        return neighbours

    def __iterate(self) -> None:
        """
        Main function that iterates the field.
        There are outcomes of this function:
            - Cells are found that can safely by opened.
            - Cells are found that are certainly mines.
            - No safe option is found, so a random cell is opened to continue.
        :return: None
        """

        # Iterate over cells
        for row in range(self.height):
            for col in range(self.width):
                if self.states[row][col] != CellState.SAFE:
                    continue

                neighbours = self.__get_neighbours(col, row)

                # Count the number of unopened neighbours. If this number is 0, continue to next cell.
                n_unopened = sum(map(lambda nb: self.states[nb[1]][nb[0]] == CellState.UNKNOWN, neighbours))
                if n_unopened == 0:
                    continue

                # Calculate probability of hitting a mine for the unopened neighbours of this cell
                n_mines = sum(map(lambda nb: self.states[nb[1]][nb[0]] == CellState.MINE, neighbours))
                n_mines_left = self.adj_mines[row][col] - n_mines
                prob = n_mines_left / n_unopened

                # Look for safe options
                if abs(prob - 1) < 1e-5:
                    # All neighbours are mines
                    for cell in neighbours:
                        if self.states[cell[1]][cell[0]] == CellState.UNKNOWN:
                            self.states[cell[1]][cell[0]] = CellState.MINE
                    return

                elif prob < 1e-5:
                    # All neighbours are safe
                    for cell in neighbours:
                        if self.states[cell[1]][cell[0]] == CellState.UNKNOWN:
                            self.__open_cell(cell[0], cell[1])
                    return

        # If program reaches this point, no safe cells or certain mines are found.
        # Pick a random unknown cell to continue.
        unknown_cells = []
        for row_i, row in enumerate(self.states):
            for col_i, state in enumerate(row):
                if state == CellState.UNKNOWN:
                    unknown_cells.append((col_i, row_i))
        guess = sample(unknown_cells, 1)[0]
        self.__open_cell(*guess)

    def __open_cell(self, col: int, row: int) -> None:
        """
        Convenience function to open a cell and set the appropriate members to keep track.
        :param col: Column index of cell to open.
        :param row: Row index of cell to open.
        :return: None
        """
        try:
            adj = self.minefield.sweep_cell(col, row)
            self.adj_mines[row][col] = adj
            self.states[row][col] = CellState.SAFE
        except mineField.ExplosionException:
            print('Boom!')
            raise GameOver

    def __is_done(self) -> bool:
        """
        Function to check if field is fully cleared.
        :return: True if field is fully cleared. False otherwise.
        """
        return sum([row.count(CellState.UNKNOWN) for row in self.states]) == 0

    def run(self) -> list:
        """
        Main function that executes the solve.
        :return: List of mine coordinates.
        """
        print("Solving minesweeper...")

        # Open centre cell to start
        self.__open_cell(self.width//2, self.height//2)

        # Iterate until game is finished or a mine is hit
        while not self.__is_done():
            try:
                self.__iterate()
            except GameOver:
                break

        self.__print()
        print("Finished :)" if self.__is_done() else 'Hit a mine :(')

        # Collect mine coordinates for output
        mine_coords = []
        for row_i, row in enumerate(self.states):
            for col_i, state in enumerate(row):
                if state == CellState.MINE:
                    mine_coords.append((col_i, row_i))

        return mine_coords
