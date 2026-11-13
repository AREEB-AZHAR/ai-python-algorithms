import chess
import math

# Material values for evaluation
piece_values = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def evaluate_board(board):
    """
    Evaluates the board state.
    Positive scores favor White, negative scores favor Black.
    """
    if board.is_checkmate():
        if board.turn:
            return -9999  # Black wins (White is currently to move and in checkmate)
        else:
            return 9999   # White wins (Black is currently to move and in checkmate)
            
    if board.is_game_over():
        return 0  # Stalemate or Draw
        
    evaluation = 0
    # Simple Material Evaluation
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                evaluation += value
            else:
                evaluation -= value
    return evaluation

def alphabeta_chess(board, depth, alpha, beta, maximizing_player):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = list(board.legal_moves)
    
    if maximizing_player: # White's turn to optimize
        max_eval = -float('inf')
        for move in moves:
            board.push(move)
            eval_score = alphabeta_chess(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break # Beta cutoff
        return max_eval
    else: # Black's turn to optimize
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval_score = alphabeta_chess(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break # Alpha cutoff
        return min_eval

def get_best_move(board, depth):
    """
    Determines the best move for the current player (White or Black).
    """
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    
    # Check whose turn it is
    is_maximizing = board.turn == chess.WHITE
    
    if is_maximizing:
        best_val = -float('inf')
    else:
        best_val = float('inf')

    # Iterate through all legal moves
    for move in board.legal_moves:
        board.push(move)
        # If current is max (White), next is min (Black), so pass False. And vice versa.
        val = alphabeta_chess(board, depth - 1, alpha, beta, not is_maximizing)
        board.pop()
        
        if is_maximizing:
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
        else:
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            
    return best_move

def print_board(board):
    print(board)
    print("\n----------------\n")

def main():
    board = chess.Board()
    
    # Choose color
    print("Welcome to Python Chess AI!")
    user_side = input("Play as White (w) or Black (b)? ").lower()
    
    if user_side == 'b':
        # AI plays first move as White
        print("AI is thinking...")
        ai_move = get_best_move(board, 3) # Depth 3 is decent for Python
        board.push(ai_move)
        print(f"AI moved: {ai_move}")
    
    while not board.is_game_over():
        print_board(board)
        
        # Human Move
        while True:
            try:
                move_uci = input("Enter your move (e.g., e2e4): ")
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    board.push(move)
                    break
                else:
                    print("Illegal move. Try again.")
            except ValueError:
                print("Invalid format. Use UCI format like 'e2e4'.")

        if board.is_game_over():
            break

        # AI Move
        print("AI is thinking...")
        # Depth 3 is a balance between speed and skill. 
        # Increase to 4 or 5 for a stronger but slower AI.
        ai_move = get_best_move(board, 3) 
        
        if ai_move is None:
            print("AI has no moves. Game Over.")
            break
            
        board.push(ai_move)
        print(f"AI moved: {ai_move}")

    print_board(board)
    print("Game Over")
    print("Result: ", board.result())

if __name__ == "__main__":
    main()