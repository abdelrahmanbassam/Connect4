from Heuristic.heuristic import Heuristic

class NormalScore(Heuristic):
    # Normal score heuristic
    def heuristic(self, board, player, col = None):
        return self.count_fours(board, player) - self.count_fours(board, 3 - player)

    def count_fours(self, board, player):
        rows, cols = len(board), len(board[0])
        score = 0

        # ROWS
        for r in range(rows):
            count = 0
            for c in range(cols):
                if board[r][c] == player:
                    count += 1
                else:
                    score += max(0, count - 3)
                    count = 0
            score += max(0, count - 3)

        # COLUMNS
        for c in range(cols):
            count = 0
            for r in range(rows):
                if board[r][c] == player:
                    count += 1
                else:
                    score += max(0, count - 3)
                    count = 0
            score += max(0, count - 3)

        # DIAGONAL \ (Top-left to bottom-right)
        for d in range(-rows + 1, cols):
            count = 0
            for r in range(rows):
                c = d + r
                if 0 <= c < cols:
                    if board[r][c] == player:
                        count += 1
                    else:
                        score += max(0, count - 3)
                        count = 0
            score += max(0, count - 3)

        # DIAGONAL / (Top-right to bottom-left)
        for d in range(cols + rows - 1):
            count = 0
            for r in range(rows):
                c = d - r
                if 0 <= c < cols:
                    if board[r][c] == player:
                        count += 1
                    else:
                        score += max(0, count - 3)
                        count = 0
            score += max(0, count - 3)

        return score

            