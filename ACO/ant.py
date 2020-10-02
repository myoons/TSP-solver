import random

class Ant(object):
    
    def __init__(self, aco, graph, tabu=None):
        """
        aco : ACO
        graph : Graph of Nodes
        """
        self.aco = aco
        self.graph = graph
        self.totalCost = 0 # Total Cost of each ant
        self.tabu = [] if tabu==None else tabu
        self.pheromoneDelta = [] # Local increase of pheromone
        self.allowed = [i for i in range(graph.nodeSize)] # Allowed nodes that ant can explore
        self.eta = [[0 if i==j else 1 / graph.costMatrix[i][j] for j in range(graph.nodeSize)] for i in range(graph.nodeSize)] # Heuristic Information

        start = random.randint(0, graph.nodeSize - 1) # Start from random node for each ant

        self.tabu.append(start)
        self.current = start # Current node of the ant
        self.allowed.remove(start)
    
    def select_next(self):
        
        denominator = 0 # Denominator of the possibility
 
        for i in self.allowed:
            denominator += (self.graph.pheromone[self.current][i] ** self.aco.alpha) * (self.eta[self.current][i] ** self.aco.beta)

        probabilities = [0 for i in range(self.graph.nodeSize)] # Initialize the proability of each node (to explore)

        for i in self.allowed:
            probabilities[i] = (self.graph.pheromone[self.current][i] ** self.aco.alpha) * (self.eta[self.current][i] ** self.aco.beta) / denominator
        
        selected = 0 # Select the next node (to explore) by roulette
        rand = random.random()

        for i, probability in enumerate(probabilities):
            
            rand -= probability
            if rand <= 0 : # i node is selected to explore
                selected = i
                break
        
        self.allowed.remove(selected) # Remove the selected node (next node to explore) from allowed
        self.tabu.append(selected)
        self.totalCost += self.graph.costMatrix[self.current][selected] # Add the cost of edge (current -> selected)
        self.current = selected

    def update_pheromone_delta(self):
        
        self.pheromoneDelta = [[0 for j in range(self.graph.nodeSize)] for i in range(self.graph.nodeSize)] # Initialize pheromoneDelta
        
        for exploredNode in range(1, len(self.tabu)):

            i = self.tabu[exploredNode - 1]
            j = self.tabu[exploredNode]

            self.pheromoneDelta[i][j] = self.aco.Q / self.graph.costMatrix[i][j] # Delta for Node i -> Node j