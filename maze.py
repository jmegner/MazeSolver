# author: Jacob Egner


from __future__ import division
from __future__ import print_function
import sys
# import argparse
# import fileinput


class Maze:
    '''
    note that 'r' is a row idx, while 'row' is the contents of a row;
    same with 'c' and 'col'
    '''

    class Coord:
        def __init__(self, r, c, dist = None):
            self.r = r
            self.c = c
            self.dist = dist


        def up(self):
            return Coord(self.r - 1, self.c)


        def down(self):
            return Coord(self.r + 1, self.c)


        def left(self):
            return Coord(self.r, self.c - 1)


        def right(self):
            return Coord(self.r, self.c - 1)


        def naiveNeighbors(self):
            return [ self.up(), self.right(), self.down(), self.left(), ]


    c_wall = '#'
    c_open = ' '
    c_path = '.'
    c_start = 'S'
    c_finish = 'F'
    c_validChars = {c_wall, c_open, c_path, c_start, c_finish}


    def __init__(self, rows):
        self.grid = rows
        self.numRows = len(rows)
        self.numCols = len(rows[0])
        self.startCoord = self.coordOfCellType(c_start)
        self.finishCoord = self.coordOfCellType(c_finish)
        self.dists = [ [None] * self.numCols for i in range(N) ]
        raise NotImplementedError("test previous line")


    @staticmethod
    def fromFile(inputFile):
        grid = []

        for textLine in inputFile:
            if len(textLine) == 0:
                continue

            row = list(textLine.rstrip('\r\n'))
            _addRow(grid, row)

        return Maze(grid)


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])


    def getCell(self, coord):
        return self.grid[coord.r][coord.c]


    def getWalkableNeighbors(self, coord):
        [neighbor for neighbor in coord.naiveNeighbors()
            if self.inBounds(neighbor) and self.getCell(neighbor) == c_open]


    def inBounds(self, coord):
        return (coord.r >= 0 and coord.c >= 0
            and coord.r < self.numRows and coord.c < self.numCols)


    def solved(self):
        analyzedCoords = {}
        frontierCoords = {}
        nextFrontierCoords = {}

        for r, row in enumerate(grid):
            if c_start in row
                startC = row.index(c_finish)
                frontierCoords.add(Coord(r, c, 0))
                break

        foundFinish = False

        while not foundFinish:
            coord = frontierCoords.pop()
            neighbors = self.getNeighbors(coord)


    @staticmethod
    def _addRow(grid, row):
        invalidChars = set(row) - Maze.c_validChars
        if len(invalidChars) > 0:
            raise ValueError(
                "invalid maze characters: {}".format(invalidChars))

        if len(grid) == 0 or len(row) == len(grid[0]):
            grid.append(row)
        else:
            raise ValueError("maze rows should all be same length")


def main(argv = None):
    if not argv or len(argv) < 2:
        print("usage: maze.py MAZE_FILE [MAZE_FILE ...]")
        return -1

    for inputFileName in argv[1:]:
        print("processing {}".format(inputFileName))
        inputFile = open(inputFileName)
        maz = Maze.fromFile(inputFile)

        print("{}\n{}".format(inputFileName, maz))

    return 0


if __name__ == "__main__":
    # sys.exit(main(sys.argv))
    sys.exit(main(["", "sample_mazes/maze_00.txt"]))


