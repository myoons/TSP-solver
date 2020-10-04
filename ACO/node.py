import math

class Node:
    
    def __init__(self, x, y):
        """
        x : x coordinate of the node
        y : y coordinate of the node
        """
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

def distance(node1, node2):
    """
    Calculating distance between two Nodes
    """
    xDistance = abs(node1.getX() - node2.getX())
    yDistance = abs(node1.getY() - node2.getY())
    return math.sqrt((xDistance*xDistance) + (yDistance*yDistance))