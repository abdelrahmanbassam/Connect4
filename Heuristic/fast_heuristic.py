from Heuristic.heuristic import Heuristic

class FastHeuristic(Heuristic):
    # Fast heuristic
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
        row = self.get_row(board, col)
        counts = self.utilization(board, player, row, col)
        counts2 = self.utilization(board, 3 - player, row, col)
        counts = [counts[i] + counts2[i] for i in range(3)]
        score = sum([counts[i] * self.weights[i+1] for i in range(3)]) + self.weights[0] * self.board_weight[row][col]
        return score

    def utilization(self, board, player, row, col):
        # frequency of 2, 3, 4 consecutive pieces
        rows, cols = len(board), len(board[0])
        count = [0, 0, 0, 0, 0, 0]
        # ROW
        left = 0
        right = 0
        curr = col - 1
        while curr >= 0 and board[row][curr] == player:
            left += 1
            curr -= 1
        curr = col + 1
        while curr < 7 and board[row][curr] == player:
            right += 1
            curr += 1
        if left + right + 1 > 1:
            count[left + right - 1] += 1
        # COLUMN
        bottom = 0
        curr = row + 1
        while curr < 6 and board[curr][col] == player:
            bottom += 1
            curr += 1
        if bottom + 1 > 1:
            count[bottom - 1] += 1
        # DIAGONAL \
        left = 0
        right = 0
        currR = row - 1
        currC = col - 1
        while currR >= 0 and currC >= 0 and board[currR][currC] == player:
            left += 1
            currR -= 1
            currC -= 1
        currR = row + 1
        currC = col + 1
        while currR < 6 and currC < 7 and board[currR][currC] == player:
            right += 1
            currR += 1
            currC += 1
        if left + right + 1 > 1:
            count[left + right - 1] += 1
        # DIAGONAL /
        left = 0
        right = 0
        currR = row - 1
        currC = col + 1
        while currR >= 0 and currC < 7 and board[currR][currC] == player:
            left += 1
            currR -= 1
            currC += 1
        currR = row + 1
        currC = col - 1
        while currR < 6 and currC >= 0 and board[currR][currC] == player:
            right += 1
            currR += 1
            currC -= 1
        if left + right + 1 > 1:
            count[left + right - 1] += 1
        return [count[0], count[1], (count[2] + 2*count[3] + 3*count[4] + 4*count[5])]

    def get_row(self, board, col):
        for i in range(6):
            if board[i][col] == 0:
                return i
        return -1