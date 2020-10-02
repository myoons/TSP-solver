from .ant import Ant

# Class of Any Colony Optimization
class ACO(object):
    
    def __init__(self, antSize, generations, alpha, beta, rho, q):
        """
        antSize : Number of Ants
        generations : Number of iterations
        alpha : Relative importance of pheromone
        beta : Relative importance of heuristic information
        rho : Residual coefficient of pheromone (Evaporatin Rate)
        q : Pheromone Intensity
        """
        self.antSize = antSize
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = q
    
    def update_pheromone(self, graph, ants):
        """
        graph : Graph of Nodes
        ants : Ants List (List of all ants)
        """
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho # Calculate the residual pheromones

                for ant in ants :
                    graph.pheromone[i][j] += ant.pheromoneDelta[i][j] # Add the pheromones of ants in each edge

    def find_fittest(self, graph):
        """
        graph : Graph of Nodes
        """
        bestCost = float('inf')
        bestSolution = []

        for gen in range(self.generations):

            ants = [Ant(self, graph, []) for i in range(self.antSize)] # Generate ants for each generation

            for ant in ants:
                # For each ant, choose thier route to explore
                for i in range(graph.nodeSize - 1): 
                    ant.select_next() 

                ant.totalCost += graph.costMatrix[ant.tabu[-1]][ant.tabu[0]] # Add the cost of last node -> start node 

                if ant.totalCost < bestCost:
                    bestCost = ant.totalCost
                    bestSolution = [] + ant.tabu

                ant.update_pheromone_delta() # Update pheromoneDelta of ants
            
            # Update pheromone in the graph
            self.update_pheromone(graph, ants)

        return bestSolution, bestCost