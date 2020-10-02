import math, random
import datetime

from ACO.node import Node, distance
from ACO.graph import Graph
from ACO.aco import ACO
from ACO.ant import Ant, Anti

def main():

    # Record the start time
    start = datetime.datetime.now()

    # Open the tsp File
    tspFile = open('./tspFiles/test.tsp', 'r')

    # Read Header
    Name = tspFile.readline().strip().split(':')[1] # Name
    Comment = tspFile.readline().strip().split(':')[1] # Comment
    FileType = tspFile.readline().strip().split(':')[1] # Type (.tsp)
    Dimension = tspFile.readline().strip().split(':')[1] # Dimension
    EdgeWeightType = tspFile.readline().strip().split(':')[1] # Edge Weight Type

    # Read Node_COORD_SECTION Line
    tspFile.readline()

    nodeSize = int(Dimension)
    nodes = []
    costMatrix = []

    for i in range(nodeSize) :
        index, x, y = tspFile.readline().strip().split()
        nodes.append(Node(x=float(x), y=float(y)))
    
    costMatrix = [[distance(nodes[i], nodes[j]) for j in range(nodeSize)] for i in range(nodeSize)] # Cost Matrix = 1/Distance

    aco = ACO(18, 10, 1.0, 5.0, 0.4817, 10, 5, 0.05)
    graph = Graph(costMatrix, nodeSize)
    path, cost = aco.find_fittest(graph)

    # Record Finish Time
    finish = datetime.datetime.now()

    print('Final Distance :', cost)
    print("Executed Time :", finish-start)

if __name__ == '__main__':
    main()