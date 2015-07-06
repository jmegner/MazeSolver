# author: Jacob Egner
# date: 2015-07-05


import collections
import copy
import itertools
import functools


@functools.total_ordering
class VeryBig:
    def __eq__(self, other): return isinstance(other, VeryBig)
    def __lt__(self, other): return False
    def __add__(self, other): return self
    def __radd__(self, other): return self


class Edge(collections.namedtuple('Edge', ['srcId', 'dstId', 'cost'])):
    pass


@functools.total_ordering
class Node:

    def __init__(self, nodeId, edges, estimatedRemainingDist = 0):
        self.nodeId = nodeId
        self.edges = edges
        self.pathParent = None
        self.currDist = VeryBig()
        self.estimatedRemainingDist = estimatedRemainingDist


    def __str__(self):
        return str(self.nodeId)


    def __repr__(self):
        return "Node(id={},parent={},currDist={},remDist={},edges={})".format(
            self.nodeId,
            self.pathParent,
            self.currDist,
            self.estimatedRemainingDist,
            self.edges);


    def __eq__(self, other):
        return self.possibleTotalPathLen() == other.possibleTotalPathLen()


    def __lt__(self, other):
        return self.possibleTotalPathLen() < other.possibleTotalPathLen()


    def possibleTotalPathLen(self):
        return self.currDist + self.estimatedRemainingDist


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
        startId, finishId,
        neighborIdsAndCostsFunc,
        estimatedRemainingDistFunc
    ):
        nodeMap = {}
        visitedNodeIds = set()
        nodeIdStack = [startId]

        while nodeIdStack:
            nodeId = nodeIdStack.pop()
            estimatedRemainingDist = estimatedRemainingDistFunc(nodeId)
            edges = [Edge(nodeId, neighborId, cost)
                for neighborId, cost in neighborIdsAndCostsFunc(nodeId)]

            nodeMap[nodeId] = Node(nodeId, edges, estimatedRemainingDist)

            visitedNodeIds.add(nodeId)

            for edge in edges:
                if edge.dstId not in visitedNodeIds:
                    nodeIdStack.append(edge.dstId)

        return AStar(nodeMap, startId, finishId)


    def solve(self):
        self._explore()
        self._markPath()


    def _explore(self):
        openNodeIds = set()

        self.nodeMap[self.startId].currDist = 0
        openNodeIds.add(self.startId)

        while openNodeIds:
            newlySolvedNode = min(map(
                lambda nodeId: self.nodeMap[nodeId],
                openNodeIds))

            if newlySolvedNode.nodeId == self.finishId:
                break

            openNodeIds.remove(newlySolvedNode.nodeId)

            for edge in newlySolvedNode.edges:
                newDist = newlySolvedNode.currDist + edge.cost
                neighbor = self.nodeMap[edge.dstId]

                if newDist < neighbor.currDist:
                    neighbor.currDist = newDist
                    neighbor.pathParent = newlySolvedNode
                    openNodeIds.add(neighbor.nodeId)


    def _markPath(self):
        if self.finishId is None:
            return

        currNode = self.nodeMap[self.finishId]
        reversePath = []

        while currNode is not None:
            reversePath.append(currNode)
            currNode = currNode.pathParent

        self.pathToFinish = list(reversed(reversePath))


