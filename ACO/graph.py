class Graph(object):
    
    def __init__(self, costMatrix, nodeSize):
        """
        nodeSize : Number of nodes (N)
        costMatrix : N*N size matrix of costs (length of edges)
        """
        self.costMatrix = costMatrix
        self.nodeSize = nodeSize
        # Initialize the pheromone in the graph
        self.pheromone = [[1/(nodeSize*nodeSize) for j in range(nodeSize)] for i in  range(nodeSize)] 