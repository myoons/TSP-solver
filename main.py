import math, random
import datetime
import csv
import argparse

from ACO.node import Node, distance
from ACO.graph import Graph
from ACO.aco import ACO

def main():

    args = parser.parse_args()

    fileName = args.t
    antSize = int(args.p)
    generations = int(args.g)
    maxFit = int(args.f)

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
    nodes = [] # List of nodes
    costMatrix = [] # N*N matrix of cost

    for i in range(nodeSize) :
        index, x, y = tspFile.readline().strip().split()
        nodes.append(Node(x=float(x), y=float(y)))
    
    costMatrix = [[distance(nodes[i], nodes[j]) for j in range(nodeSize)] for i in range(nodeSize)] # Cost Matrix = 1/Distance

    aco = ACO(antSize, generations, maxFit, 1.0, 8.0, 0.5, 10, 5) # Main Structure
    graph = Graph(costMatrix, nodeSize) # Graph of the nodes
    path, cost = aco.find_fittest(graph) # Solve TSP problem

    # Record Finish Time
    finish = datetime.datetime.now()
    
    # Print the best Cost (total length)
    print(cost)
    print(finish-start)

    # Write solution in csv file
    f = open('solution'+'_'+fileName.split('.')[0]+'.csv','w',newline='')
    wr = csv.writer(f)
    for node in path:
        wr.writerow([node+1])

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-t', required=True, help="File Name (TSP)")
    parser.add_argument('-p', required=True, help="Number of Ants")
    parser.add_argument('-g', required=True, help='Number of Generations')
    parser.add_argument('-f', required=True, help='Max Number of Fitness Function')
    
    main()
    
        