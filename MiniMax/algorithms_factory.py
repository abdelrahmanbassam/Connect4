from MiniMax.MiniMaxWoPruning import MiniMaxWoPruning
from MiniMax.MiniMaxWithPruning import MiniMaxWithPruning
from MiniMax.MiniMax import MiniMax
from Heuristic.heuristic import Heuristic


class AlgorithmsFactory:
    # Factory class for creating search algorithms
    def get_algorithm(self, algorithm_id, heuristic, board, player, max_depth):
        if algorithm_id == 1:
            return MiniMaxWoPruning(heuristic, board, player, max_depth)
        elif algorithm_name == "MiniMaxWithPruning":
            return MiniMaxWithPruning(heuristic, board, player, max_depth)
        
        

