from Heuristic.heuristics_factory import HeuristicsFactory
from Tree import Node
class MiniMax:
    def __init__(self, heuristic, board, player, max_depth):
        self.heuristic = heuristic
        self.board = board
        self.player = player
        self.max_depth = max_depth
        self.sign = 1 if player == 1 else -1
        self.best_move = None
        self.root = None
        self.nodes_expanded = 0
    
    def maximize(self, board, depth, root):
        pass
    def minimize(self, board, depth, root):
        pass
    def minimax(self, board, depth):
        root = Node(float('-inf'), "MAX")
        self.nodes_expanded += 1
        score, move = self.maximize(board, depth, root)
        self.best_move = move
        self.root = root
        print(root.visualize())
        return move

    def is_terminal(self, board):
        return board[0].count(0) == 0
    
    def get_possible_moves(self, board):
        return [c for c in range(len(board[0])) if board[0][c] == 0]

    def make_move(self, board, move, player):
        new_board = [row[:] for row in board]
        for r in range(len(new_board) - 1, -1, -1):
            if new_board[r][move] == 0:
                new_board[r][move] = player
                break
        return new_board
    
    def opponent(self, player):
        return 1 if player == 2 else 2
    def tree_to_graph(self, root):
        nodes = {}
        edges = {}
        node_counter = 1
        edge_counter = 1

        def traverse(node, parent_id=None):
            nonlocal node_counter, edge_counter

            # Create a unique node ID
            current_node_id = f"node{node_counter}"
            node_counter += 1

            # Add current node to the nodes dictionary with `value` as `name` and `type`
            nodes[current_node_id] = {
                "name": str(node.value),  # Convert the value to string for the name
                "type": node.type,        # Add type (min/max)
                "icon": "&#xe5c7" if node.type == "MAX" else "&#xe5c5" if node.type == "MIN" else ""
            }

            # If there's a parent, add an edge from the parent to the current node
            if parent_id is not None:
                edge_id = f"edge{edge_counter}"
                edges[edge_id] = {"source": parent_id, "target": current_node_id}
                edge_counter += 1

            # Traverse child nodes
            for successor in node.successors:
                traverse(successor, current_node_id)

        # Start traversal from the root
        traverse(root)
        return {"nodes": nodes, "edges": edges}
