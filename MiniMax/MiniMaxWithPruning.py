from MiniMax.MiniMax import MiniMax
from Heuristic.heuristics_factory import HeuristicsFactory
class MiniMaxWithPruning(MiniMax):
    def __init__(self, heuristic, board, player, max_depth):
        super().__init__(heuristic, board, player, max_depth)

    def maximize(self, board, depth, alpha = float('-inf'), beta = float('inf')):
        if depth == 0 or self.is_terminal(board):
            return self.heuristic.heuristic(board) * self.sign, None

        best_move = None
        max_score = float('-inf')
        for move in self.get_possible_moves(board):
            new_board = self.make_move(board, move, self.player)
            score, _ = self.minimize(new_board, depth - 1, alpha, beta)
            alpha = max(alpha, score)
            if score > max_score:
                max_score = score
                best_move = move
            if alpha >= beta:
                break
        return max_score, best_move

    def minimize(self, board, depth, alpha = float('-inf'), beta = float('inf')):
        if depth == 0 or self.is_terminal(board):
            return self.heuristic.heuristic(board) * self.sign, None

        best_move = None
        min_score = float('inf')
        for move in self.get_possible_moves(board):
            new_board = self.make_move(board, move, self.opponent(self.player))
            score, _ = self.maximize(new_board, depth - 1,alpha, beta)
            beta = min(beta, score)
            if score < min_score:
                min_score = score
                best_move = move
            if alpha >= beta:
                break
        return min_score, best_move
    