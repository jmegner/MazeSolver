# author: Jacob Egner


from __future__ import division
from __future__ import print_function
import collections
import copy
import sys


class Maze:
    '''
    note that 'r' is a row idx, while 'row' is the contents of a row;
    same with 'c' and 'col'
    '''


    c_maxDist = 1e99
    c_wall = '#'
    c_open = ' '
    c_path = '.'
    c_start = 'S'
    c_finish = 'F'
    c_validInputChars = {c_wall, c_open, c_start, c_finish}


    RcTuple = collections.namedtuple('RcTuple', ['r', 'c'])

    class Coord(RcTuple):

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


    def __init__(self, cells):
        'cells is 2d list of chars'

        self.cells = cells

        self.numRows = len(cells)
        self.numCols = len(cells[0])

        #self.startCoord = self.coordOfCellType(self.c_start)
        #self.finishCoord = self.coordOfCellType(self.c_finish)

        self.dists = [ [self.c_maxDist] * self.numCols
            for i in range(self.numRows) ]
        self.pathedCells = copy.deepcopy(self.cells)
        self.pathCoords = []


    @staticmethod
    def fromFile(inputFile):
        cells = []

        for textLine in inputFile:
            if len(textLine) == 0:
                continue

            row = list(textLine.rstrip('\r\n'))
            Maze._addRow(cells, row)

        return Maze(cells)


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.pathedCells])


    def getCell(self, coord):
        return self.cells[coord.r][coord.c]


    def getDist(self, coord):
        return self.dists[coord.r][coord.c]


    def setDist(self, coord, dist):
        self.dists[coord.r][coord.c] = dist


    def getWalkableNeighbors(self, coord):
        [self.Coord(neighbor.r, neighbor.c, self.getDist(neighbor))
                for neighbor in coord.naiveNeighbors()
                if self.inBounds(neighbor) and self.getCell(neighbor) == c_open]


    def inBounds(self, coord):
        return (coord.r >= 0 and coord.c >= 0
            and coord.r < self.numRows and coord.c < self.numCols)


    def getMinDistCoord(self, coords):
        min(coords,
            key = lambda a, b : a if self.getDist(a) < self.getDist(b) else b)


    def solve(self):
        solvedCoords = set()
        unsolvedCoords = set()

        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == self.c_start:
                    self.dists[r][c] = 0
                else:
                    self.dists[r][c] = self.c_maxDist

                if self.cells[r][c] != self.c_wall:
                    unsolvedCoords.add(self.Coord(r, c))

        foundFinish = False

        while not foundFinish and unsolvedCoords:
            newlySolvedCoord = self.getMinDistCoord(unsolvedCoords)
            newFrontierDist = self.getDist(newlySolvedCoord) + 1

            unsolvedCoords.remove(newlySolvedCoord)
            solvedCoords.add(newlySolvedCoord)

            neighbors = self.getWalkableNeighbors(newlySolvedCoord)

            for neighbor in neighbors:
                if newFrontierDist < neighbor.dist:
                    self.setDist(neighbor, newFrontierDist)

                    if self.getCell(neighbor) == self.c_finish:
                        foundFinish = True
                        break


    @staticmethod
    def _addRow(cells, row):
        invalidChars = set(row) - Maze.c_validInputChars
        if len(invalidChars) > 0:
            raise ValueError(
                "invalid maze characters: {}".format(invalidChars))

        if len(cells) == 0 or len(row) == len(cells[0]):
            cells.append(row)
        else:
            raise ValueError("maze rows should all be same length")


def main(argv = None):
    if not argv or len(argv) < 2:
        print("usage: maze.py MAZE_FILE [MAZE_FILE ...]")
        return -1

    if True:
        fiddleVar = 7
    print("fiddleVar={}".format(fiddleVar))

    for inputFileName in argv[1:]:
        print("processing {}".format(inputFileName))
        inputFile = open(inputFileName)
        maz = Maze.fromFile(inputFile)

        print("{}\n{}".format(inputFileName, maz))
        maz.solve()

    return 0


if __name__ == "__main__":
    # sys.exit(main(sys.argv))
    sys.exit(main(["", "sample_mazes/maze_00.txt"]))


