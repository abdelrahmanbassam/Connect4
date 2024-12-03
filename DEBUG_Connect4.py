from Heuristic.heuristics_factory import HeuristicsFactory
from MiniMax.algorithms_factory import AlgorithmsFactory

def print_board(board):
    """
    Print the current state of the board in a user-friendly format.
    """
    print("\n".join([" ".join(map(str, row)) for row in board]))
    print("-" * 20)

def is_full(board):
    """
    Check if the board is completely filled.
    """
    return all(cell != 0 for row in board for cell in row)

if __name__ == "__main__":
    # Create the factory objects
    algorithms_factory = AlgorithmsFactory()
    heuristics_factory = HeuristicsFactory()

    # Initialize the game
    heuristic = heuristics_factory.get_heuristic("ConsecutiveCounts")
    board = [[0 for _ in range(7)] for _ in range(6)]  # 6x7 Connect Four board
    player = 1  # Human player
    ai_player = 2  # AI player
    max_depth = 4

    algorithm = algorithms_factory.get_algorithm(2, heuristic, board, ai_player, max_depth)

    print("Welcome to Connect Four! You are Player 1.")
    print_board(board)

    while True:
        # Human's turn
        while True:
            try:
                human_move = int(input("Enter your move (0-6): "))
                if 0 <= human_move < 7 and board[0][human_move] == 0:
                    break
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")

        # Make the human move
        for r in range(len(board) - 1, -1, -1):
            if board[r][human_move] == 0:
                board[r][human_move] = player
                break

        print("Your move:")
        print_board(board)

        if is_full(board):
            print("The board is full! Game over.")
            break

        # AI's turn
        print("AI is making its move...")
        best_move = algorithm.minimax(board, max_depth)
        for r in range(len(board) - 1, -1, -1):
            if board[r][best_move] == 0:
                board[r][best_move] = ai_player
                break

        print("AI's move:")
        print_board(board)
        print("Nodes expanded: " + str(algorithm.nodes_expanded))

        if is_full(board):
            print("The board is full! Game over.")
            break
