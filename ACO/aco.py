from .ant import Ant
import random

# Class of Any Colony Optimization
class ACO(object):
    
    def __init__(self, antSize, generations, alpha, beta, rho, q):
        """
        antSize : Number of Ants
        generations : Number of iterations
        alpha : Relative importance of pheromone
        beta : Relative importance of heuristic information
        rho : Residual coefficient of pheromone (Evaporatin Rate)
        q : Amount of pheromone that each ant has
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

    def weaken_suboptim(self, graph, subOptim):
        """
        graph : Graph of Nodes
        subOptim : route of subOptimal
        """
        for node in range(1, len(subOptim)):
    
            i = subOptim[node - 1]
            j = subOptim[node]
                    
            graph.pheromone[i][j] *= self.rho
    
    def strengthen_optim(self, graph, optim):
        """
        graph : Graph of Nodes
        optim : route of current optimal
        """
        for node in range(1, len(optim)):
    
            i = optim[node - 1]
            j = optim[node]
                    
            graph.pheromone[i][j] *= (1/self.rho)

    def find_fittest(self, graph):
        """
        graph : Graph of Nodes
        """
        bestCost = float('inf')
        bestSolution = []

        for gen in range(self.generations):

            ants = [Ant(self, graph) for i in range(self.antSize)] # Generate ants for each generation

            for ant in ants:
                # For each ant, choose thier route to explore
                for i in range(graph.nodeSize - 1): 
                    ant.select_next(graph.eta) 

                ant.totalCost += graph.costMatrix[ant.tabu[-1]][ant.tabu[0]] # Add the cost of last node -> start node 

                if ant.totalCost < bestCost:
                    
                    # Weaken the suboptim to make sure not selected
                    self.weaken_suboptim(graph, bestSolution)
                    self.strengthen_optim(graph, ant.tabu)

                    bestCost = ant.totalCost
                    bestSolution = ant.tabu

                ant.update_pheromone_delta() # Update pheromoneDelta of ants

            # Update pheromone in the graph
            self.update_pheromone(graph, ants)

        return bestSolution, bestCost