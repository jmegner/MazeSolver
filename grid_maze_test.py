# author: Jacob Egner


import unittest
from grid_maze import *


class LocTest(unittest.TestCase):

    def testManhattanDist(self):
        locA = Loc(3, 5)
        locB = Loc(-7, -11)
        self.assertEqual(locA.manhattanDist(locB), 26)


class GridMazeTest(unittest.TestCase):

    s_grid1Cells = [
        #     0123456789
        list("##########"), #  0
        list("#   S#F   "), #  1
        list("#    #    "), #  2
        list("#    #    "), #  3
        list("#  ###### "), #  4
        list("#    #    "), #  5
        list("#    #    "), #  6
        list("#    #    "), #  7
        list("#         "), #  8
        list("#         "), #  9
        list("#         "), # 10
        ]

    s_grid1PossiblePathedCells = [
        #     0123456789
        list("##########"), #  0
        list("# ..S#F..."), #  1
        list("# ...#...."), #  2
        list("# ...#...."), #  3
        list("# .######."), #  4
        list("# ...#...."), #  5
        list("# ...#...."), #  6
        list("# ...#...."), #  7
        list("# ........"), #  8
        list("#         "), #  9
        list("#         "), # 10
        ]

    s_grid1StartLoc = Loc(1, 4)
    s_grid1FinishLoc = Loc(1, 6)
    s_grid1BestPathLen = 26


    def setUp(self):
        self.maze = GridMaze(self.s_grid1Cells)


    def testInBounds(self):
        self.assertTrue(self.maze.inBounds(Loc(0, 0)))
        self.assertFalse(self.maze.inBounds(Loc(-1, 0)))
        self.assertFalse(self.maze.inBounds(Loc(0, -1)))
        self.assertFalse(self.maze.inBounds(Loc(99, 0)))
        self.assertFalse(self.maze.inBounds(Loc(0, 99)))


    def testIsWalkable(self):
        self.assertFalse(self.maze.isWalkable(Loc(0, 0)))
        self.assertFalse(self.maze.isWalkable(Loc(99, 99)))
        self.assertTrue(self.maze.isWalkable(self.s_grid1StartLoc))
        self.assertTrue(self.maze.isWalkable(self.s_grid1FinishLoc))


    def testSolvePathGood(self):
        self.maze.solve()

        # test that path is short enough
        self.assertEqual(len(self.maze.pathLocs), self.s_grid1BestPathLen + 1)

        numPathCells = sum([self.maze.pathedCells[r][c] == self.maze.c_path
            for r in range(self.maze.numRows)
            for c in range(self.maze.numCols)])

        # test that length of path matches pathedCells
        self.assertEqual(numPathCells, len(self.maze.pathLocs) - 2)

        # test that path starts and ends correctly
        self.assertTrue(self.maze.pathLocs[0] == self.s_grid1StartLoc)
        self.assertTrue(self.maze.pathLocs[-1] == self.s_grid1FinishLoc)

        for currLoc, prevLoc in zip(
                self.maze.pathLocs[1:], self.maze.pathLocs[0:-1]):
            # test locs contiguous
            self.assertEqual(currLoc.manhattanDist(prevLoc), 1)

            # test loc is compatible with pathedCells
            self.assertTrue(
                self.maze.pathedCells[currLoc.r][currLoc.c]
                in self.maze.c_pathLikeTypes)

            # test loc is compatible with our precomputed possible path cells
            self.assertTrue(
                self.s_grid1PossiblePathedCells[currLoc.r][currLoc.c]
                in self.maze.c_pathLikeTypes)


if __name__ == '__main__':
    unittest.main()


