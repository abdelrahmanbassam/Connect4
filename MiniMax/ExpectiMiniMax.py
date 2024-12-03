from MiniMax.MiniMax import MiniMax
from Heuristic.heuristics_factory import HeuristicsFactory
from Tree import Node
from Heuristic.fast_heuristic import FastHeuristic
class ExpectiMiniMax(MiniMax):
    def __init__(self, heuristic, board, player, max_depth,):
        super().__init__(heuristic, board, player, max_depth)
        self.FastHeuristic = HeuristicsFactory().get_heuristic("FastHeuristic")
        
    def chance(self, board, selected_move, next_turn_maximizing:bool, root, depth, extra):
        probs = {"left": 0.2, "right": 0.2, "current": 0.6}
        chance_node = Node(0.0, "CHANCE", selected_move)
        root.add_successor(chance_node) # root is MIN OR MAX

        player = self.opponent(self.player) if next_turn_maximizing else self.player
        def call_next_turn(new_board, depth, chance_node, next_turn_maximizing, chance_to_move, extra):
            if next_turn_maximizing:
                child = Node(float('-inf'), "MAX", chance_to_move)
                chance_node.add_successor(child)
                score, _ = self.maximize(new_board, depth-1, child, extra)
            else:
                child = Node(float('inf'), "MIN", chance_to_move)
                chance_node.add_successor(child)
                score, _ = self.minimize(new_board, depth-1, child, extra)
            return score
        
        # either the current move is played
        # --> we make the move and call minimize if next turn is min
        new_board = self.make_move(board, selected_move, player)
        self.nodes_expanded += 1
        score = call_next_turn(new_board, depth, chance_node, next_turn_maximizing, selected_move, extra)  
        score_current = score

        # if the left to selected move is possible to play
        # we play it
        score_left =  None
        if selected_move - 1 >= 0 and board[0][selected_move - 1] == 0:
            new_board = self.make_move(board, selected_move-1, player)
            self.nodes_expanded += 1
            score = call_next_turn(new_board, depth, chance_node, next_turn_maximizing, selected_move - 1, extra) 
            score_left = score

        score_right = None
        if selected_move + 1 < len(self.board[0]) and board[0][selected_move + 1] == 0:
            new_board = self.make_move(board, selected_move + 1, player)
            self.nodes_expanded += 1
            score = call_next_turn(new_board, depth, chance_node, next_turn_maximizing, selected_move + 1, extra) 
            score_right = score

        # make sure the probabilitiess are normalized
        if score_right is not None and score_left is not None:
            # both left and right are valid
            probs["left"] = 0
            probs["right"] = 0
            probs["current"] = 1
        elif score_right is not None:
            # only right is valid (left is invalid)
            probs["left"] = 0
            probs["right"] = probs["right"] / (probs["right"] + probs["current"])
            probs["current"] = 1-probs["right"] 
            score_left = 0
        elif score_left is not None:
            # only left is valid (right is invalid)
            probs["right"] = 0
            probs["left"] = probs["left"] / (probs["left"] + probs["current"])
            probs["current"] = 1-probs["left"] 
            score_right = 0
        else:
            # both left and right are invalid
            probs["right"] = 0
            probs["left"] = 0
            probs["current"] = 1
            score_left = 0
            score_right = 0
        score = probs["current"]*score_current+probs["left"]*score_left+probs["right"]*score_right
        chance_node.value = score
        return score

    def maximize(self, board, depth, root, extra = 0):
        # if self.hash_board(board) in self.cache:
        #     root.value, best = self.cache[self.hash_board(board)]
        #     return root.value, best
        if depth == 0 or self.is_terminal(board):
            score = (self.heuristic.heuristic(board, self.player) + extra) * self.sign
            root.value = score
            self.cache[self.hash_board(board)] = score, None
            return score, None

        best_move = None
        max_score = float('-inf')
        # print(self.cache)
        for move in self.get_possible_moves(board):
            extra = self.FastHeuristic.heuristic(board, self.player, move)
            self.nodes_expanded += 1
            score = self.chance(board, move, False, root, depth - 1, extra)
            if score > max_score:
                max_score = score
                best_move = move
        root.value = max_score
        self.cache[self.hash_board(board)] = max_score, best_move
        return max_score, best_move

    def minimize(self, board, depth, root, extra = 0):
        # if self.hash_board(board) in self.cache:
        #     root.value, best = self.cache[self.hash_board(board)]
        #     return root.value, best
        if depth == 0 or self.is_terminal(board):
            score = (self.heuristic.heuristic(board, self.player) + extra)* self.sign
            root.value = score
            self.cache[self.hash_board(board)] = score, None
            return score, None
        # print(self.cache)
        best_move = None
        min_score = float('inf')
        for move in self.get_possible_moves(board):
            extra = self.FastHeuristic.heuristic(board, self.player, move)
            self.nodes_expanded += 1
            score = self.chance(board, move, True, root, depth - 1, extra)
            if score < min_score:
                min_score = score
                best_move = move
        root.value = min_score
        self.cache[self.hash_board(board)] = min_score, best_move
        return min_score, best_move
    