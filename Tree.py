class Node:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.successors = []
    
    def add_successor(self, successor):
        self.successors.append(successor)
        
    def visualize(self, depth=0, prefix=""):
        """
        Recursively visualize the tree structure.
        """
        indent = "    " * depth
        result = f"{indent}{prefix}(value={self.value})\n"
        for i, child in enumerate(self.successors):
            result += child.visualize(depth + 1, prefix=f"{child.type} {i+1}: ")
        return result