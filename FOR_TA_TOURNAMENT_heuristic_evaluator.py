from MiniMax.MiniMaxWithPruning import MiniMaxWithPruning
from Heuristic.heuristics_factory import HeuristicsFactory
from MiniMax.algorithms_factory import AlgorithmsFactory

MAX_DEPTH = 9
algorithms_factory = AlgorithmsFactory()
heuristics_factory = HeuristicsFactory()
heuristic = heuristics_factory.get_heuristic("ConsecutiveCounts")

def play_best_move(board:list) -> int: 
    global MAX_DEPTH, algorithms_factory, heuristic
    # Using Alpha beta Pruning algorithm:
    algorithm = algorithms_factory.get_algorithm(2, heuristic, board, 2, MAX_DEPTH)
    # Zero indexed column 
    return algorithm.minimax(board, MAX_DEPTH)

if __name__ == '__main__':
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0],
        [0, 0, 1, 2, 1, 0, 0],
        [1, 2, 1, 1, 2, 2, 0]
    ]
    print("Evaluating for board: ")
    for row in board:
        print(row)
    best_move = play_best_move(board)
    # Zero index
    print("Best move is column:", best_move)
