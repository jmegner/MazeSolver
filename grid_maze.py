# author: Jacob Egner
# date: 2015-07-05


import collections
import copy
import sys
import graph


class Loc(collections.namedtuple('Rc', ['r', 'c'])):

    def north(self): return Loc(self.r - 1, self.c)
    def south(self): return Loc(self.r + 1, self.c)
    def west(self): return Loc(self.r, self.c - 1)
    def east(self): return Loc(self.r, self.c + 1)

    def cardinalNeighbors(self):
        return [ self.north(), self.east(), self.south(), self.west(), ]


    def principalNeighbors(self):
        return [Loc(r + delR, c + delC) for delR, delC
            in itertools.product([-1, 0, 1], repeat=2) if delR or delC]


    def manhattanDist(self, other):
        return abs(self.r - other.r) + abs(self.c - other.c)


class GridMaze:

    c_maxDist = 1e99
    c_wall = '#'
    c_open = ' '
    c_path = '.'
    c_start = 'S'
    c_finish = 'F'
    c_validInputChars = {c_wall, c_open, c_start, c_finish}
    c_walkableTypes = {c_open, c_start, c_finish}
    c_pathLikeTypes = {c_path, c_start, c_finish}


    def __init__(self, cells):
        'cells is 2d list of chars'

        self.cells = copy.deepcopy(cells)

        self.numRows = len(cells)
        self.numCols = len(cells[0])

        self.startLoc = self.getLocOfCellType(self.c_start)
        self.finishLoc = self.getLocOfCellType(self.c_finish)

        self.solvedCells = copy.deepcopy(self.cells)

        self._aStar = None


    @staticmethod
    def fromFile(inputFile):
        cells = []

        for textLine in inputFile:
            if len(textLine) == 0:
                continue

            row = list(textLine.rstrip('\r\n'))
            GridMaze._addRow(cells, row)

        return GridMaze(cells)


    def __str__(self):
        return '\n'.join([''.join(row) for row in self.solvedCells])


    def getCell(self, loc):
        return self.cells[loc.r][loc.c]


    def inBounds(self, loc):
        return (loc.r >= 0 and loc.c >= 0
            and loc.r < self.numRows and loc.c < self.numCols)


    def isWalkable(self, loc):
        return (self.inBounds(loc)
            and self.getCell(loc) != self.c_wall)


    def getWalkableNeighbors(self, loc):
        return [neighbor for neighbor in loc.cardinalNeighbors()
                if self.isWalkable(neighbor)]


    def getLocOfCellType(self, cellType):
        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == cellType:
                    return Loc(r, c)
        return None


    def solve(self):
        def neighborIdsAndCosts(loc):
            walkableNeighbors = self.getWalkableNeighbors(loc)
            return zip(walkableNeighbors, [1] * len(walkableNeighbors))

        def estimatedRemainingDist(loc):
            return self.finishLoc.manhattanDist(loc)

        self._aStar = graph.AStar.fromGrid(
            self.cells,
            self.startLoc,
            self.finishLoc,
            neighborIdsAndCosts,
            estimatedRemainingDist)

        self._aStar.solve()

        self.solvedCells = copy.deepcopy(self.cells)

        for node in self._aStar.pathToFinish:
            loc = node.nodeId
            if loc not in [self.startLoc, self.finishLoc]:
                self.solvedCells[loc.r][loc.c] = self.c_path


    @staticmethod
    def _addRow(cells, row):
        invalidChars = set(row) - GridMaze.c_validInputChars
        if len(invalidChars) > 0:
            raise ValueError(
                "invalid maze characters: {}".format(invalidChars))

        if len(cells) == 0 or len(row) == len(cells[0]):
            cells.append(row)
        else:
            raise ValueError("maze rows should all be same length")


def main(argv = None):
    if not argv or len(argv) < 2:
        print("usage: grid_maze.py MAZE_FILE [MAZE_FILE ...]")
        return -1

    for inputFileName in argv[1:]:
        print("processing {}".format(inputFileName))
        inputFile = open(inputFileName)
        maze = GridMaze.fromFile(inputFile)

        print("{}\n{}".format(inputFileName, maze))

        maze.solve()

        print("\n{}".format(maze))

    return 0


if __name__ == "__main__":
    # sys.exit(main(sys.argv))
    sys.exit(main([
        "",
        "sample_mazes/maze_00.txt",
        "sample_mazes/maze_01.txt",
        "sample_mazes/maze_02.txt",
        ]))


