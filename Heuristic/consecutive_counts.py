from Heuristic.heuristic import Heuristic

class ConsecutiveCounts(Heuristic):
    # Consecutive counts heuristic
    def __init__(self):
        self.weights = [1, 10, 1000, 1000000]
        self.board_weight = [
            [3, 4, 5, 7, 5, 4, 3],
            [4, 6, 8, 10, 8, 6, 4],
            [5, 8, 11, 13, 11, 8, 5],
            [5, 8, 11, 13, 11, 8, 5],
            [4, 6, 8, 10, 8, 6, 4],
            [3, 4, 5, 7, 5, 4, 3]
        ]
    def heuristic(self, board, player, col = None):
        counts = self.count_consecutive(board, player)
        location_points = self.location_points(board, player)
        score = location_points * self.weights[0] 
        score += counts[0] * self.weights[1]
        score += counts[1] * self.weights[2]
        score += counts[2] * self.weights[3]
        return score

    def location_points(self, board, player):
        sum = 0
        for i in range(6):
            for j in range(7):
                if board[i][j] == player:
                    sum +=self. board_weight[i][j]
                elif board[i][j] == 3 - player:
                    sum -= self.board_weight[i][j]
        return sum

    def count_consecutive(self, board, player):
        # frequency of 2, 3, 4 consecutive pieces
        rows, cols = len(board), len(board[0])
        count = [0, 0, 0]
        
        # ROWS
        for r in range(rows):
            temp = self.count_row(board[r], player)
            count[0] += temp[0]
            count[1] += temp[1]
            count[2] += temp[2]
        
        # COLUMNS
        for c in range(cols):
            temp = self.count_row([board[r][c] for r in range(rows)], player)
            count[0] += temp[0]
            count[1] += temp[1]
            count[2] += temp[2]
        
        # DIAGONAL \ (Top-left to bottom-right)
        for d in range(-rows + 1, cols):
            temp = self.count_row([board[r][d + r] for r in range(rows) if 0 <= d + r < cols], player)
            count[0] += temp[0]
            count[1] += temp[1]
            count[2] += temp[2]

        # DIAGONAL / (Top-right to bottom-left)
        for d in range(cols + rows - 1):
            temp = self.count_row([board[r][d - r] for r in range(rows) if 0 <= d - r < cols], player)
            count[0] += temp[0]
            count[1] += temp[1]
            count[2] += temp[2]
        return count

    def count_row(self, row, player):
        count = [0, 0, 0, 0, 0, 0]
        curr_player = 0
        curr_count = 1
        for i in range(len(row)):
            if curr_player == row[i]:
                if curr_player != 0:
                    curr_count += 1
            else:
                if curr_player != 0 and curr_count > 1:
                    if curr_player == player:
                        count[curr_count - 2] += 1
                    else:
                        count[curr_count - 2] -= 1
                curr_player = row[i]
                curr_count = 1
        if curr_player != 0 and curr_count > 1:
            if curr_player == player:
                count[curr_count - 2] += 1
            else:
                count[curr_count - 2] -= 1
        # 5 = 2 fours, 6 = 3 fours, 7 = 4 fours
        # print(count)
        return [count[0], count[1], (count[2]+(2*count[3])+(3*count[4])+(4*count[5]))]