import math

# Class Node (City)
class Node:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

# Distance between two Nodes
def distance(node1, node2):
    xDistance = abs(node1.getX() - node2.getX())
    yDistance = abs(node1.getY() - node2.getY())
    return math.sqrt((xDistance*xDistance) + (yDistance*yDistance))