import chess
import math
import pygame
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 600
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
BOARD_COLORS = [(240, 217, 181), (181, 136, 99)] # Light, Dark (Wood theme)
HIGHLIGHT_COLOR = (100, 249, 83, 100) # Green highlight with transparency

# --- CHESS LOGIC & AI ---

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
            return -9999  # Black wins
        else:
            return 9999   # White wins
            
    if board.is_game_over():
        return 0  # Stalemate or Draw
        
    evaluation = 0
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
    """Minimax algorithm with Alpha-Beta Pruning."""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = list(board.legal_moves)
    
    if maximizing_player:
        max_eval = -float('inf')
        for move in moves:
            board.push(move)
            eval_score = alphabeta_chess(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval_score = alphabeta_chess(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth):
    """Determines the best move for the current player."""
    best_move = None
    alpha = -float('inf')
    beta = float('inf')
    is_maximizing = board.turn == chess.WHITE
    
    best_val = -float('inf') if is_maximizing else float('inf')

    for move in board.legal_moves:
        board.push(move)
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

# --- PYGAME GRAPHICS ---

def draw_board(screen):
    """Draws the checkerboard pattern."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = BOARD_COLORS[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, font):
    """Draws pieces using Unicode characters."""
    # Unicode mapping
    piece_unicode = {
        'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
        'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece_unicode[piece.symbol()]
            # Adjust color: Black pieces are drawn black, White pieces are drawn white (with outline usually, but font color works)
            # Since we are using text, we can force the font color.
            # However, standard chess font glyphs often have fill. 
            # To ensure visibility on the wood board:
            if piece.color == chess.WHITE:
                text_color = (255, 255, 255)
            else:
                text_color = (0, 0, 0)
            
            text_surface = font.render(symbol, True, text_color)
            
            # Mathematical conversion from 0-63 square index to x,y
            # chess.A1 is 0 (bottom left). chess.H8 is 63 (top right).
            # File (col): square % 8
            # Rank (row): square // 8
            file_idx = chess.square_file(square)
            rank_idx = chess.square_rank(square)
            
            # Pygame coordinates: Row 0 is top. Rank 7 is top.
            c = file_idx
            r = 7 - rank_idx 
            
            text_rect = text_surface.get_rect(center=(c*SQ_SIZE + SQ_SIZE//2, r*SQ_SIZE + SQ_SIZE//2))
            screen.blit(text_surface, text_rect)

def highlight_square(screen, square):
    """Highlights a selected square."""
    if square is not None:
        file_idx = chess.square_file(square)
        rank_idx = chess.square_rank(square)
        c = file_idx
        r = 7 - rank_idx
        
        s = pygame.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100) # Transparency
        s.fill(pygame.Color('yellow'))
        screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

def draw_text_center(screen, text):
    """Draws text in the center of the screen (for Game Over)."""
    font = pygame.font.SysFont("Arial", 32, bold=True)
    text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    
    # Background box
    bg_rect = text_rect.inflate(20, 20)
    pygame.draw.rect(screen, (255, 255, 255), bg_rect)
    pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)
    
    screen.blit(text_surface, text_rect)

# --- MAIN GAME LOOP ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI")
    clock = pygame.time.Clock()
    
    # Try to load a font that supports unicode chess symbols well. 
    # 'Segoe UI Symbol' is good on Windows, 'Apple Symbols' on Mac, 'DejaVu Sans' on Linux.
    # Fallback to default system font if specific ones aren't found.
    font_name = pygame.font.match_font('segoe ui symbol', 'apple symbols', 'dejavu sans')
    font = pygame.font.Font(font_name, int(SQ_SIZE * 0.8))

    board = chess.Board()
    selected_square = None
    player_turn = True # True if it's player's turn (White), False if AI (Black)
    
    running = True
    game_over = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Human Input Handler
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn:
                location = pygame.mouse.get_pos() # (x, y)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                
                # Convert Pygame row (0-7 top-down) to Chess Rank (7-0 bottom-up)
                rank = 7 - row
                file = col
                clicked_square = chess.square(file, rank)
                
                if selected_square == clicked_square:
                    selected_square = None # Deselect
                else:
                    if selected_square is not None:
                        # Attempt move
                        move = chess.Move(selected_square, clicked_square)
                        
                        # Handle Promotion (Auto-promote to Queen for simplicity)
                        if board.piece_at(selected_square).piece_type == chess.PAWN:
                            if (board.turn == chess.WHITE and rank == 7) or \
                               (board.turn == chess.BLACK and rank == 0):
                                move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)
                        
                        if move in board.legal_moves:
                            board.push(move)
                            player_turn = False # Switch to AI
                            selected_square = None
                        else:
                            # If invalid move, select the new piece if it belongs to player
                            piece = board.piece_at(clicked_square)
                            if piece and piece.color == board.turn:
                                selected_square = clicked_square
                            else:
                                selected_square = None
                    else:
                        # Select piece
                        piece = board.piece_at(clicked_square)
                        if piece and piece.color == board.turn:
                            selected_square = clicked_square

        # Draw Game State
        draw_board(screen)
        highlight_square(screen, selected_square)
        draw_pieces(screen, board, font)
        
        if board.is_game_over():
            game_over = True
            result = board.result()
            draw_text_center(screen, f"Game Over: {result}")
        
        pygame.display.flip()
        
        # AI Logic (Triggered after screen update so we see the player's move)
        if not player_turn and not game_over:
            # Small delay or visual indicator could go here
            pygame.event.pump() # Prevent freeze warning
            
            # AI Thinking...
            ai_move = get_best_move(board, 3) # Depth 3
            if ai_move:
                board.push(ai_move)
                player_turn = True
            else:
                game_over = True
        
        clock.tick(MAX_FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()