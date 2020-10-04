import random

class Ant(object):
    
    def __init__(self, aco, graph):
        """
        (param) aco : the main structure that ant is included
        (param) graph : Graph of Nodes
        totalCost : total cost of the ant (Smaller, Better)
        tabu : List of nodes in sequence that ant explored
        pheromoneDelta : N*N matrix that has information about increased pheromones in each edge by this ant 
        allowed : List of nodes that this ant didn't explored yet
        """
        self.aco = aco
        self.graph = graph
        self.totalCost = 0 # Initialize 0
        self.tabu = [] # List of nodes in sequence of exploration
        self.pheromoneDelta = [] # Local increase of pheromone
        self.allowed = [i for i in range(graph.nodeSize)] # Allowed nodes that ant can explore

        start = random.randint(0, graph.nodeSize - 1) # Start from random node for each ant

        self.tabu.append(start)
        self.current = start # Current node of the ant
        self.allowed.remove(start) # Since ant started (explored the node), remove from allowed
    
    """
    # Bad , Not used

    I tried to select the next node by tournament selection to prevent ant sticking in local optima at first
    But the result was bad.
    So this function is not used
    """
    def tournamentSelection(self, probList):
        """
        (param) probList : List of probabilities
        """
        nonZeroList = []
        tempList = []

        for prob in probList:    
            if prob != 0 :
                nonZeroList.append(probList.index(prob))
        
        for i in range(16):
            randomId = int(random.random() * len(nonZeroList))
            tempList.append(nonZeroList[randomId])
        
        sortedList = sorted(tempList)

        return sortedList[0]

    def select_next(self, eta):
        
        """
        (param) eta : The heuristic information about the graph

        Function for ant to select the next node
        """
        denominator = 0 # Denominator of the probabilites (Sum of all proababilites)
 
        for i in self.allowed:
            denominator += (self.graph.pheromone[self.current][i] ** self.aco.alpha) * (eta[self.current][i] ** self.aco.beta)

        probabilities = [0 for i in range(self.graph.nodeSize)] # Initialize the proability of each node

        for i in self.allowed:
            probabilities[i] = (self.graph.pheromone[self.current][i] ** self.aco.alpha) * (eta[self.current][i] ** self.aco.beta) / denominator
        
        selected = 0 # Node selected to explore next
        rand = random.random() # random number for random roulette  
        randOpt = random.random() # random number for selecting the next node 

        # Probability of 0.9 to choose the max node
        if randOpt < 0.9 : 
            selected = probabilities.index(max(probabilities))
        else : # Random roulette
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
        """
        Function for updating the pheromoneDetla of the ant.
        Amount of pheromones that ant have is equal.
        Among edges that ant explored, short edge gets larger pheromoneDelta and long edge gets smaller pheromoneDetla
        """
        self.pheromoneDelta = [[0 for j in range(self.graph.nodeSize)] for i in range(self.graph.nodeSize)] # Initialize pheromoneDelta
        
        for exploredNode in range(1, len(self.tabu)):
            
            i = self.tabu[exploredNode - 1]
            j = self.tabu[exploredNode]

            self.pheromoneDelta[i][j] = self.aco.Q / self.graph.costMatrix[i][j] # Delta for Node i -> Node j


                

                