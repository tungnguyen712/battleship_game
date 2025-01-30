from battleship import *
import copy

def terminal(board):
    for row in board:
        if 'S' in row:
            return False
    return True

def utility(board):
    score = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "X":
                score += 10
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    if 0 <= i+dx < len(board) and 0 <= j+dy < len(board):
                        if board[i+dx][j+dy] == "~":
                            score += 3
            elif board[i][j] == "O":
                score -= 2
    return score

def actions(board, hits):
    moves = []
    for (r, c) in hits:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board) and board[nr][nc] == '~':
                if (nr, nc) not in moves:
                    moves.append((nr, nc))
    if not moves:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == '~' and (i, j) not in moves:
                    moves.append((i, j))
    return moves

def simulate_result(board, row, col, hits):
    new_board = copy.deepcopy(board)
    new_hits = copy.deepcopy(hits)
    if new_board[row][col] == "S":
        new_board[row][col] = "X"
        if (row, col) not in new_hits:
            new_hits.append((row, col))
    else:
        new_board[row][col] = "O"
    return new_board, new_hits

def minimax(board, hits, misses):
    best_score = -float('inf')
    best_action = None
    if terminal(board):
        return None
    for action in actions(board, hits):
        new_board, new_hits = simulate_result(board, action[0], action[1], hits)
        score = min_value(new_board, new_hits, misses, depth=1, alpha=-float('inf'), beta=float('inf'))
        if score > best_score:
            best_score = score
            best_action = action
    return best_action

max_depth = 4

def min_value(board, hits, misses, depth=0, alpha=-float('inf'), beta=float('inf')):
    if terminal(board) or depth >= max_depth:
        return utility(board)
    v = float('inf')
    for action in actions(board, hits):
        new_board, new_hits = simulate_result(board, action[0], action[1], hits)
        v = min(v, max_value(new_board, new_hits, misses, depth + 1, alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def max_value(board, hits, misses, depth=0, alpha=-float('inf'), beta=float('inf')):
    if terminal(board) or depth >= max_depth:
        return utility(board)
    v = -float('inf')
    for action in actions(board, hits):
        new_board, new_hits = simulate_result(board, action[0], action[1], hits)
        v = max(v, min_value(new_board, new_hits, misses, depth + 1, alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v