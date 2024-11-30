from flask import Flask, request, jsonify
from MiniMax.MiniMax import MiniMax
from Heuristic.heuristics_factory import HeuristicsFactory
from MiniMax.algorithms_factory import AlgorithmsFactory

app = Flask(__name__)

@app.route('/api/game/move', methods=['POST'])
def make_move():
    try:
        # Extract the board and current player from the request
        data = request.json
        board = data.get("board")
        algorithm = data.get("algorithm", 1)
        turn = data.get("aiTurn", 1)
        max_depth = data.get("depth", 3)

        # Set up MiniMax
        heuristic = HeuristicsFactory().get_heuristic("NormalScore")
        algorithm = AlgorithmsFactory().get_algorithm(algorithm, heuristic, board, turn, max_depth)
        best_move = algorithm.minimax(board, max_depth)
        nodes_expanded = algorithm.nodes_expanded
        board = algorithm.make_move(board, best_move, turn)
        player1_score = heuristic.count_fours(board, 1)
        player2_score = heuristic.count_fours(board, 2)

        return jsonify({
            "col": best_move,
            "player1_score": player1_score,
            "player2_score": player2_score,
            "nodes_expanded": nodes_expanded,
            "tree": " "
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
