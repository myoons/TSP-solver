import math, random
import datetime
import csv
import argparse

from ACO.node import Node, distance
from ACO.graph import Graph
from ACO.aco import ACO

######################################################################
# Options
######################################################################


################################

def main():

    args = parser.parse_args()

    fileName = args.f
    antSize = int(args.p)
    generations = int(args.g)

    # Record the start time
    start = datetime.datetime.now()

    # Open the tsp File
    tspFile = open('./tspFiles/'+fileName, 'r')

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

    aco = ACO(antSize, generations, 1.0, 8.0, 0.4817, 10, 5, 0.05)
    graph = Graph(costMatrix, nodeSize)
    path, cost = aco.find_fittest(graph)

    # Record Finish Time
    finish = datetime.datetime.now()
    
    # Print the best Cost (total length)
    print(cost)
    print(finish-start)

    # Write solution in csv file
    f = open('solution'+'_'+fileName.split('.')[0]+'.csv','w',newline='')
    wr = csv.writer(f)
    for node in path:
        wr.writerow([node])

if __name__ == '__main__':

    main()

