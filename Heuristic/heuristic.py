from abc import ABC, abstractmethod

class Heuristic:
    
    @abstractmethod
    def heuristic(self, board, player):
        pass