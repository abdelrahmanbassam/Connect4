from Heuristic.heuristics_factory import HeuristicsFactory
from MiniMax.algorithms_factory import AlgorithmsFactory

if __name__ == "__main__":
    # Create the factory objects
    algorithms_factory = AlgorithmsFactory()
    heuristics_factory = HeuristicsFactory()
    # Get the heuristic object
    heuristic = heuristics_factory.get_heuristic("NormalScore")
    board = [[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0]]
    player = 1
    max_depth = 4
    # Get the algorithm object
    algorithm = algorithms_factory.get_algorithm("MiniMax", heuristic, board, player, max_depth)
    best_move = algorithm.minimax(board, max_depth)
    print(best_move)