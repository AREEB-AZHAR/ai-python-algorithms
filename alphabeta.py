import math

# Initialize 8x8 Board
board = [[" " for _ in range(8)] for _ in range(8)]
# Simple setup for demonstration (Rows 0-2: AI 'O', Rows 5-7: Player 'X')
for r in range(3):
    for c in range(8):
        if (r + c) % 2 == 1: board[r][c] = "O"
for r in range(5, 8):
    for c in range(8):
        if (r + c) % 2 == 1: board[r][c] = "X"

def print_board(board):
    print("  0 1 2 3 4 5 6 7")
    for idx, row in enumerate(board):
        print(f"{idx}|{'|'.join(row)}|")
    print("-" * 17)

def evaluate_board(board):
    # Material advantage: AI (O) wants positive, Player (X) wants negative
    ai_score = sum(row.count("O") for row in board)
    player_score = sum(row.count("X") for row in board)
    return ai_score - player_score

def get_possible_moves(board, player):
    # Simplified move generator: finds empty spots adjacent to pieces
    # In a real game, this would strictly follow movement rules
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                # Check diagonals (simplified for generic board game context)
                potential_moves = [(r+1, c-1), (r+1, c+1), (r-1, c-1), (r-1, c+1)]
                for pr, pc in potential_moves:
                    if 0 <= pr < 8 and 0 <= pc < 8 and board[pr][pc] == " ":
                        # Create a new board state for this move
                        new_board = [row[:] for row in board]
                        new_board[pr][pc] = player
                        new_board[r][c] = " "
                        moves.append(new_board)
    return moves

# Alpha-Beta Pruning Algorithm
def alphabeta(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = -math.inf
        # Generate moves for AI ('O')
        moves = get_possible_moves(board, "O")
        if not moves: return evaluate_board(board)
        
        for move in moves:
            eval = alphabeta(move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Pruning
        return max_eval
    else:
        min_eval = math.inf
        # Generate moves for Player ('X')
        moves = get_possible_moves(board, "X")
        if not moves: return evaluate_board(board)

        for move in moves:
            eval = alphabeta(move, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break # Pruning
        return min_eval

# Test the evaluation
print("Initial Board:")
print_board(board)
score = alphabeta(board, 3, -math.inf, math.inf, True)
print(f"Board Evaluation Score (Depth 3): {score}")
