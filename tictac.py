import math

# Initialize the board
board = [[" " for _ in range(3)] for _ in range(3)]

def print_board():
    """Prints the current state of the board."""
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)

def check_winner(board):
    """Checks for a winner and returns 'X', 'O', or None."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
            
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
        
    return None

def is_full(board):
    """Checks if the board is full (Draw condition)."""
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    """
    Minimax algorithm to determine the best move.
    Returns a score: +10 for AI win, -10 for Human win, 0 for Draw.
    Adjusted by depth to prefer winning sooner or losing later.
    """
    winner = check_winner(board)
    if winner == "O": # AI wins
        return 10 - depth
    if winner == "X": # Human wins
        return depth - 10
    if is_full(board): # Draw
        return 0

    if is_maximizing:
        best_score = -float('inf') # Use float('inf') for compatibility
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf') # Use float('inf') for compatibility
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    """Executes the best move for the AI."""
    best_score = -float('inf')
    best_move = None
    
    # Check all available spots
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    if best_move:
        board[best_move[0]][best_move[1]] = "O"

def player_move():
    """Handles the player's input."""
    while True:
        try:
            user_input = input("Enter row and column (0-2) separated by space: ")
            row, col = map(int, user_input.split())
            
            if 0 <= row <= 2 and 0 <= col <= 2:
                if board[row][col] == " ":
                    board[row][col] = "X"
                    break
                else:
                    print("Cell occupied! Try again.")
            else:
                print("Coordinates out of range. Use 0, 1, or 2.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter two numbers (e.g., '1 1').")

def main():
    print("Tic-Tac-Toe: You are 'X', AI is 'O'")
    print_board()

    while True:
        # Player Turn
        player_move()
        print_board()
        if check_winner(board) == "X":
            print("You Win!") 
            break
        if is_full(board):
            print("It's a Draw!")
            break

        # AI Turn
        print("AI is thinking...")
        ai_move()
        print_board()
        if check_winner(board) == "O":
            print("AI Wins!")
            break
        if is_full(board):
            print("It's a Draw!")
            break

if __name__ == "__main__":
    main()