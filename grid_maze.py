# author: Jacob Egner


import collections
import copy
import sys


RcTuple = collections.namedtuple('Rc', ['r', 'c'])

class Loc(RcTuple):

    def up(self):
        return Loc(self.r - 1, self.c)


    def down(self):
        return Loc(self.r + 1, self.c)


    def left(self):
        return Loc(self.r, self.c - 1)


    def right(self):
        return Loc(self.r, self.c + 1)


    def naiveNeighbors(self):
        return [ self.up(), self.right(), self.down(), self.left(), ]


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

        self.dists = [ [self.c_maxDist] * self.numCols
            for i in range(self.numRows) ]
        self.pathedCells = copy.deepcopy(self.cells)
        self.pathLocs = []


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
        return '\n'.join([''.join(row) for row in self.pathedCells])


    def prettyDists(self):
        prettyGrid = ""

        for r in range(self.numRows):
            for c in range(self.numCols):
                dist = self.dists[r][c]

                if dist == self.c_maxDist:
                    prettyGrid += "    X"
                else:
                    prettyGrid += "{:>5d}".format(dist)

            prettyGrid += "\n"

        return prettyGrid


    def getCell(self, loc):
        return self.cells[loc.r][loc.c]


    def isWalkable(self, loc):
        return (self.inBounds(loc)
            and self.getCell(loc) != self.c_wall)


    def getDist(self, loc):
        return self.dists[loc.r][loc.c]


    def setDist(self, loc, dist):
        self.dists[loc.r][loc.c] = dist


    def minPossibleRemainingDist(self, loc):
        return loc.manhattanDist(self.finishLoc)


    def getWalkableNeighbors(self, loc):
        return [Loc(neighbor.r, neighbor.c)
                for neighbor in loc.naiveNeighbors()
                if self.isWalkable(neighbor)]


    def inBounds(self, loc):
        return (loc.r >= 0 and loc.c >= 0
            and loc.r < self.numRows and loc.c < self.numCols)


    def getMinDistLoc(self, locs):
        return min(locs, key = self.getDist)


    def getMinEstimatedTotalDistLoc(self, locs):
        return min(locs, key = lambda loc
            : self.getDist(loc) + self.minPossibleRemainingDist(loc))


    def getLocOfCellType(self, cellType):
        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == cellType:
                    return Loc(r, c)
        return None


    def solve(self):
        self._computeBestDists()
        self._indicatePath()


    def _computeBestDists(self):
        openLocs = set()

        for r in range(self.numRows):
            for c in range(self.numCols):
                if self.cells[r][c] == self.c_start:
                    self.dists[r][c] = 0
                    openLocs.add(Loc(r, c))
                else:
                    self.dists[r][c] = self.c_maxDist

        foundFinish = False

        while not foundFinish and openLocs:
            newlySolvedLoc = self.getMinEstimatedTotalDistLoc(openLocs)

            if self.getCell(newlySolvedLoc) == self.c_finish:
                foundFinish = True
                break

            newFrontierDist = self.getDist(newlySolvedLoc) + 1

            openLocs.remove(newlySolvedLoc)

            neighbors = self.getWalkableNeighbors(newlySolvedLoc)

            for neighbor in neighbors:
                if newFrontierDist < self.getDist(neighbor):
                    self.setDist(neighbor, newFrontierDist)

                    openLocs.add(neighbor)


    def _indicatePath(self):
        if self.getDist(self.finishLoc) == self.c_maxDist:
            return

        currLoc = self.finishLoc
        reversePath = []

        while currLoc != self.startLoc:
            if currLoc != self.finishLoc:
                self.pathedCells[currLoc.r][currLoc.c] = self.c_path

            reversePath.append(currLoc)

            currLoc = self.getMinDistLoc(
                self.getWalkableNeighbors(currLoc))

        reversePath.append(self.startLoc)
        self.pathLocs = list(reversed(reversePath))


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

        print("dists:\n{}".format(maze.prettyDists()))
        print("\n{}".format(maze))

    return 0


if __name__ == "__main__":
    # sys.exit(main(sys.argv))
    sys.exit(main([
        "",
        "sample_mazes/maze_00.txt",
        "sample_mazes/maze_01.txt",
        ]))


