class Graph(object):
    
    def __init__(self, costMatrix, nodeSize):
        """
        costMatrix : N*N size matrix of costs (length of edges)
        nodeSize : Number of nodes (N)
        pheromone : amounts of pheromones in each edge / Initialize when Graph is maded
        eta : Heuristic Information that is used to make shorter edge have more pheromones
        """
        self.costMatrix = costMatrix
        self.nodeSize = nodeSize
        self.pheromone = [[1/(nodeSize*nodeSize) for j in range(nodeSize)] for i in  range(nodeSize)] # Initialize the pheromone in the graph
        self.eta = [[0 if i==j else 1 / (costMatrix[i][j] ** 2) for j in range(nodeSize)] for i in range(nodeSize)] # Heuristic Information