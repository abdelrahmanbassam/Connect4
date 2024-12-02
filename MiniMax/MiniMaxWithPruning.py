from MiniMax.MiniMax import MiniMax
from Heuristic.heuristics_factory import HeuristicsFactory
from Heuristic.fast_heuristic import FastHeuristic
from Tree import Node

class MiniMaxWithPruning(MiniMax):
    def __init__(self, heuristic, board, player, max_depth):
        super().__init__(heuristic, board, player, max_depth)
        self.FastHeuristic = HeuristicsFactory().get_heuristic("FastHeuristic")

    def maximize(self, board, depth, root, alpha=float('-inf'), beta=float('inf'), extra=0):
        if depth == 0 or self.is_terminal(board):
            score = (self.heuristic.heuristic(board, self.player) + extra) * self.sign
            root.value = score
            return score, None
        best_move = None
        max_score = float('-inf')
        for move in self.get_possible_moves(board):
            extra = self.FastHeuristic.heuristic(board, self.player, move)
            new_board = self.make_move(board, move, self.player)
            child = Node(float('inf'), "MIN", move)
            root.add_successor(child)
            self.nodes_expanded += 1

            score, _ = self.minimize(new_board, depth - 1, child, alpha, beta, extra)
            alpha = max(alpha, score)
            if score > max_score:
                max_score = score
                best_move = move
            if alpha >= beta:
                break
        root.value = max_score
        return max_score, best_move

    def minimize(self, board, depth, root, alpha=float('-inf'), beta=float('inf'), extra=0):
        if depth == 0 or self.is_terminal(board):
            score = (self.heuristic.heuristic(board, self.opponent(self.player)) + extra) * self.sign
            root.value = score
            return score, None

        best_move = None
        min_score = float('inf')
        for move in self.get_possible_moves(board):
            extra = self.FastHeuristic.heuristic(board, self.opponent(self.player), move)
            new_board = self.make_move(board, move, self.opponent(self.player))
            child = Node(float('-inf'), "MAX", move)
            root.add_successor(child)
            score, _ = self.maximize(new_board, depth - 1, child, alpha, beta, extra)
            beta = min(beta, score)
            if score < min_score:
                min_score = score
                best_move = move
            if alpha >= beta:
                break
        root.value = min_score
        return min_score, best_move