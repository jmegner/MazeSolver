# author: Jacob Egner


import collections
import copy
import itertools


class Edge(collections.namedtuple('Edge', ['srcId', 'dstId', 'cost'])):
    pass


class Node:

    def __init__(self, nodeId, edges, estimatedRemainingDist = 0):
        self.nodeId = nodeId
        self.edges = edges
        self.pathParent = None
        self.estimatedRemainingDist = estimatedRemainingDist
        self.bestDist = None


    def __str__(self):
        return str(self.nodeId)


    def __repr__(self):
        return "Node(id={},parent={},bestDist={},remDist={},edges={})".format(
            self.nodeId,
            self.pathParent,
            self.bestDist,
            self.estimatedRemainingDist,
            self.edges);


    def getNeighborIds(self):
        return [edge.dstId for edge in self.edges]


class AStar:

    def __init__(self, nodeMap, startId, finishId = None):
        '''
        nodeMap is a dict with nodeId keys and Node values;
        finishId being None indicates a desire to calculate shortest dist to
        every node rather than halting once finding a shortest path to a
        particular finish node
        '''
        self.nodeMap = copy.deepcopy(nodeMap)
        self.startId = startId
        self.finishId = finishId
        self.pathToFinish = None


    @staticmethod
    def fromGrid(
        grid,
        startR, startC, finishR, finishC,
        isNodeableFunc,
        neighborAndCostsFunc,
        estimatedRemainingDistFunc
    ):
        raise NotImplementedError('''
            think about multiple starts, multiple finishes, and whether to
            nodify every grid cell, or to do a basic iterative
            is-reachable-from-start sweep of nodifying grid cells
            ''')
        nodeMap = {}
        numR = len(grid)
        numC = len(grid[0])

        startId = (startR, startC)

        if finishR is None or finishC is None:
            finishId = None
        else
            finishId = (finishR, finishC)

        for r, c in itertools.product(range(numR), range(numC)):
            if isNodeableFunc(grid, r, c):
                nodeId = (r, c)
                edges = [Edge(srcId=nodeId, dstId=(r2, c2), cost=cost)]
                estimatedRemainingDist = estimatedRemainingDistFunc(
                    grid, r, c, finishR, finishC)

                nodeMap[nodeId] = Node(nodeId, edges, estimatedRemainingDist)

        return AStar(nodeMap, startId, finishId)


    def solve(self):
        openNodes = set()

        self.nodeMap[self.startId].bestDist = 0


