from .ant import Ant
import random

# Class of Any Colony Optimization
class ACO(object):
    
    def __init__(self, antSize, generations, maxFit, alpha, beta, rho, q, cycle):
        """
        (param) antSize : Number of Ants
        (param) generations : Number of iterations
        (param) maxFit : Max number of fitness function
        (param) alpha : Relative importance of pheromone
        (param) beta : Relative importance of heuristic information
        (param) rho : Residual coefficient of pheromone (Evaporatin Rate)
        (param) q : Amount of pheromone that each ant has
        (param) cycle : Cycle of renewal
        """
        self.antSize = antSize
        self.generations = generations
        self.maxFit = maxFit
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = q
        self.cycle = cycle

    def tabu_search(self, graph, bestSolution):
        """
        (param) graph : graph of the nodes
        (param) bestSolution : List of nodes : Current best Solution

        Function for decreasing pheromones in optimal solution.
        Half of the edges that have high costs in optimal solutions are decreased in probability of 0.5 
        """
 
        costList = [] # List of tuples about edges in best Solution (start node, end node, cost) 

        for node in range(1, len(bestSolution)):
    
            i = bestSolution[node - 1] # start node
            j = bestSolution[node] # end node

            costList.append((i, j, graph.costMatrix[i][j]))

        costList.append((bestSolution[-1], bestSolution[0], graph.costMatrix[bestSolution[-1]][bestSolution[0]])) # Adding the last edge
        sortedList = sorted(costList, key=lambda cost: cost[2], reverse=True) # Sort in descending order of cost

        size = int(len(sortedList))

        for i in range(int(size/2)):
            (i, j, cost) = sortedList[0]

            if random.random() < 0.5 : # half of edges are decreased
                graph.pheromone[i][j] *= (self.rho**6) # About 1/64

    def update_pheromone(self, graph, ants):
        """
        (param) graph : Graph of Nodes
        (param) ants : Ants List (List of all ants)

        Function for updating pheromone information in the graph
        After each generation finishes
        """
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho # Calculate the residual pheromones (Due to evaporation)

                for ant in ants :
                   graph.pheromone[i][j] += ant.pheromoneDelta[i][j] # Add the pheromones of ants in each edge

    """
    # Bad , Not used

    I tried to update the pheromone of graph for per ant.
    Becuase I thought this would make the convergence faster.
    But the result was bad.
    So this function is not used
    """
    def update_pheromone_oneAnt(self, graph, ant):
        """
        (param) graph : Graph of Nodes
        (param) ant : Ant
        """
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho # Calculate the residual pheromones
                graph.pheromone[i][j] += ant.pheromoneDelta[i][j] # Add the pheromones of ants in each edge

    def weaken_suboptim(self, graph, subOptim):
        """
        (param) graph : Graph of Nodes
        (param) subOptim : route of subOptimal

        Weakening (Decreasing the pheromones) the sub optimal soltuon.
        It will help to converge faster
        """
        for node in range(1, len(subOptim)):
    
            i = subOptim[node - 1] # start node
            j = subOptim[node] # end node
                    
            graph.pheromone[i][j] *= self.rho # decrease (Evaporate once)

        graph.pheromone[subOptim[-1]][subOptim[0]] *= self.rho # decrease (Evaporate once)

    def strengthen_optim(self, graph, optim):
        """
        (param) graph : Graph of Nodes
        (param) optim : route of current optimal solution

        Strengthening (Increasing the pheromones) the current optimal soltuon.
        It will help to converge faster
        """
        for node in range(1, len(optim)):
    
            i = optim[node - 1] # start node
            j = optim[node] # end node
                    
            graph.pheromone[i][j] *= (1/self.rho) # Increase
        
        graph.pheromone[optim[-1]][optim[0]] *= (1/self.rho) # Increase

    def find_fittest(self, graph):
        """
        (param) graph : Graph of Nodes

        Main function.
        It generates ants iterate for number of generations.
        Also per cycle, it decreases the amounts of pheromone in best solution
        """

        bestCost = float('inf')
        bestSolution = []

        count = 0 # Count whether to run tabu_search function.
        first = True # If first, there would be no weaken, and strengthen
        fitNum = 0 # Number of Fitness function called

        for gen in range(self.generations):

            if count < self.cycle: # If not cycle
                count += 1
            else: # If cycle, run tabu_search
                count = 1
                print('Tabu Search Updated')
                self.tabu_search(graph, bestSolution)

            ants = [Ant(self, graph) for i in range(self.antSize)] # Generate ants for each generation

            for ant in ants:
                for i in range(graph.nodeSize - 1): 
                    ant.select_next(graph.eta) # Coose its route to explore 

                ant.totalCost += graph.costMatrix[ant.tabu[-1]][ant.tabu[0]] # Add the cost of last node -> start node (Return)
                fitNum += 1
                print('gen :',gen,'cost :',ant.totalCost)
                
                if ant.totalCost < bestCost: # If new best solution has found
                    if not first: # If it is no first, if there is a sub optimal solution
                        self.weaken_suboptim(graph, bestSolution) # Weaken the suboptim to make sure not selected
                        self.strengthen_optim(graph, ant.tabu) # Strengthen the optimal solution that found currently

                    bestCost = ant.totalCost
                    bestSolution = ant.tabu
                    first = False
                    
                    print('update\t','gen :', gen, 'bestCost :', bestCost)

                ant.update_pheromone_delta() # Update pheromoneDelta of each ant

                if fitNum > self.maxFit: # Break the for loop when number if fitness function reached the limit
                    break
            
            if fitNum > self.maxFit: # Break the for loop when number if fitness function reached the limit
                    break

            self.update_pheromone(graph, ants) # Update pheromone in the graph after one generation based on pheromone delta inforamtion of ants

        return bestSolution, bestCost