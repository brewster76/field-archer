__author__ = 'Nick Dajda'

from random import random

class MineField:
    """Manages a map of the field. Where mines are, which spaces have been discovered and flagged.

    Convention for field array:
        '.' = no mines, has not been stepped upon or marked
        0-8 = Had been stepped on. Value is number of adjacent squares containing mines
        'x' = mine
        'f' = flagged
    """

    def __init__(self, width=10, height=10, mines=10):
        self.width = width
        self.height = height
        self.mines = mines

        # Layout is: field[row][col]
        self.field = [['.' for x in xrange(self.width)] for x in xrange(self.height)]

        # Set the mines
        assert (self.mines < self.width * self.height), "Too many mines for field to accommodate"

        # Populate mines
        mines_sown = 0
        row = col = 0
        chance = float(self.mines) / (self.width * self.height)

        while mines_sown < self.mines:
            # Roll the die
            if random() < chance:
                if self.field[row][col] is not 'x':
                    self.field[row][col] = 'x'
                    mines_sown += 1

            col += 1
            if self.width == col:
                col = 0
                row += 1

                if self.height == row:
                    row = 0

    def print_field(self):
        for row in range(0, self.height):
            text = ""
            for col in range(0, self.width):
                text = text + str(self.field[row][col])
            print text

    def step(self, row, col):
        "Here goes..."
        if 'x' == self.field[row][col]:
            return True

        if '.' == self.field[row][col]:
            self.field[row][col] = self.count_neighbouring_mines(row, col)

            if 0 == self.field[row][col]:
                self.explore_further(row, col)

        return False

    def count_neighbouring_mines(self, row, col):
        mine_count = 0

        mine_count += self.mine_in_cell(row - 1, col - 1)
        mine_count += self.mine_in_cell(row - 1, col)
        mine_count += self.mine_in_cell(row - 1, col + 1)

        mine_count += self.mine_in_cell(row, col - 1)
        mine_count += self.mine_in_cell(row, col + 1)

        mine_count += self.mine_in_cell(row + 1, col - 1)
        mine_count += self.mine_in_cell(row + 1, col)
        mine_count += self.mine_in_cell(row + 1, col + 1)

        return mine_count

    def mine_in_cell(self, row, col):
        "Mainly an error checking function to see if row and col are valid"
        if (row < 0) or (row >= self.height) or (col < 0) or (col >= self.width):
            return 0

        if 'x' == self.field[row][col]:
            return 1

        return 0

    def explore_further(self, row, col):
        assert(0 == self.field[row][col]), "Can only explore from cells already marked as 0"

        if row > 0:
            self.map_area(row-1, col)

        if row < (self.height-1):
            self.map_area(row+1, col)

        if col > 0:
            self.map_area(row, col-1)

        if col < (self.width-1):
            self.map_area(row, col+1)

    def map_area(self, row, col):
        assert (((row < 0) or (row >= self.height) or (col < 0) or (col >= self.width)) is False), \
            "Can only explore cells within the grid (row=%d, col=%d, self.height=%d, self.width=%d)" \
            % (row, col, self.height, self.width)

        # Already explored cell
        if self.field[row][col] is not '.':
            return

        self.field[row][col] = self.count_neighbouring_mines(row, col)

        if 0 == self.field[row][col]:
            self.explore_further(row, col)

mf = MineField(40, 10, 20)

if mf.step(3, 4):
    print "Bang!"

mf.print_field()
