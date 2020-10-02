from .ant import Ant, Anti
import random

# Class of Any Colony Optimization
class ACO(object):
    
    def __init__(self, antSize, generations, alpha, beta, rho, q, tournamentSize, mutationRate):
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
        self.tournamentSize = tournamentSize
        self.mutationRate = mutationRate
    
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

    def tournamentSelection(self, costSol):
        """
        costSol : List of (cost,solution) tuples
        """
        tempList = []

        for i in range(0, self.tournamentSize) :
            randomId = int(random.random() * len(costSol))
            tempList.append(costSol[randomId])
        
        sortedList = sorted(tempList, key=lambda sol: sol[0])

        return sortedList[0][1]

    def mutation(self, sol):
        """
        sol : solution (List of nodes in sequence of explor)
        """
        for firstPoint in range(len(sol)):

            if random.random() < self.mutationRate:
                secondPoint = int(random.random() * len(sol))

                nodeOne = sol[firstPoint]    
                nodeTwo = sol[secondPoint]

                sol[secondPoint] = nodeOne
                sol[firstPoint] = nodeTwo

    def crossover(self, solOne, solTwo) :


        solChild = []

        startPos = int(random.random() * len(solOne))
        endPos = int(random.random() * len(solOne))

        for i in range(0, len(solOne)) :

            if startPos < endPos and i > startPos and i < endPos :
                solChild.append(solOne[i])
            elif startPos > endPos :
                if not (i < startPos and i > endPos) :
                    solChild.append(solOne[i])
        
        for i in range(0, len(solTwo)) :
            
            if not solTwo[i] in solChild :
                solChild.append(solTwo[i])
        
        return solChild


    def find_fittest(self, graph):
        """
        graph : Graph of Nodes
        """
        bestCost = float('inf')
        bestSolution = []
        costSol = []

        for gen in range(self.generations):
            
            if (gen%2):

                sol1 = self.tournamentSelection(costSol)
                sol2 = self.tournamentSelection(costSol)
                sol3 = self.tournamentSelection(costSol)
                sol4 = self.tournamentSelection(costSol)

                ants = []
                perSize = int(self.antSize/6)

                for i in range(perSize):
                    child = self.crossover(sol1, sol2)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))
                
                for i in range(perSize):
                    child = self.crossover(sol1, sol3)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))

                for i in range(perSize):
                    child =  self.crossover(sol1, sol4)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))
                
                for i in range(perSize):
                    child = self.crossover(sol2, sol3)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))
                
                for i in range(perSize):
                    child = self.crossover(sol2, sol4)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))

                for i in range(perSize):
                    child =  self.crossover(sol3, sol4)
                    self.mutation(child)
                    ants.append(Anti(self, graph, child))

                for ant in ants:
                    
                    ant.total_cost() # Calculate total cost
                    ant.totalCost += graph.costMatrix[ant.tabu[-1]][ant.tabu[0]] # Add the cost of last node -> start node 

                    if ant.totalCost < bestCost:
                        bestCost = ant.totalCost
                        bestSolution = ant.tabu
                    
                    ant.update_pheromone_delta() # Update pheromoneDelta of ants
            
            else:   

                ants = [Ant(self, graph) for i in range(self.antSize)] # Generate ants for each generation

                for ant in ants:
                    # For each ant, choose thier route to explore
                    for i in range(graph.nodeSize - 1): 
                        ant.select_next() 

                    ant.totalCost += graph.costMatrix[ant.tabu[-1]][ant.tabu[0]] # Add the cost of last node -> start node 

                    costSol.append((ant.totalCost, ant.tabu))

                    if ant.totalCost < bestCost:
                        bestCost = ant.totalCost
                        bestSolution = ant.tabu

                    ant.update_pheromone_delta() # Update pheromoneDelta of ants
                
                # Update pheromone in the graph
                self.update_pheromone(graph, ants)

        return bestSolution, bestCost