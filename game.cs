using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace GameCollection
{
    class Program
    {
        static void Main(string[] args)
        {
            while (true)
            {
                Console.Clear();
                Console.WriteLine("===========================");
                Console.WriteLine("   THREE GAMES ARCADE (C#) ");
                Console.WriteLine("===========================");
                Console.WriteLine("1. Card Flip & Match (Memory)");
                Console.WriteLine("2. Connect the Dots (Connect 4)");
                Console.WriteLine("3. Tic-Tac-Toe");
                Console.WriteLine("4. Exit");
                Console.WriteLine("===========================");

                int choice = GetIntInput("Select a game (1-4): ", 1, 4);

                switch (choice)
                {
                    case 1:
                        MemoryGame game1 = new MemoryGame();
                        game1.Play();
                        break;
                    case 2:
                        ConnectFour game2 = new ConnectFour();
                        game2.Play();
                        break;
                    case 3:
                        TicTacToe game3 = new TicTacToe();
                        game3.Play();
                        break;
                    case 4:
                        Console.WriteLine("Thanks for playing! Goodbye.");
                        return;
                }
            }
        }

        // Helper for input validation
        public static int GetIntInput(string prompt, int min, int max)
        {
            while (true)
            {
                Console.Write(prompt);
                string input = Console.ReadLine();
                if (int.TryParse(input, out int result) && result >= min && result <= max)
                {
                    return result;
                }
                Console.WriteLine($"Invalid input. Please enter a number between {min} and {max}.");
            }
        }
    }

    // ==========================================
    // GAME 1: MEMORY MATCH
    // ==========================================
    class MemoryGame
    {
        const int Rows = 4;
        const int Cols = 4;
        List<string> board;
        bool[] revealed;
        bool[] matched;

        public MemoryGame()
        {
            string[] symbols = { "A", "A", "B", "B", "C", "C", "D", "D",
                                 "E", "E", "F", "F", "G", "G", "H", "H" };
            Random rnd = new Random();
            board = symbols.OrderBy(x => rnd.Next()).ToList();
            revealed = new bool[16];
            matched = new bool[16];
        }

        void DrawBoard()
        {
            Console.Clear();
            Console.WriteLine("=== MEMORY CARD FLIP ===");
            Console.WriteLine("Find all matching pairs!\n");
            Console.WriteLine("   0 1 2 3");
            Console.WriteLine("  ---------");
            for (int r = 0; r < Rows; r++)
            {
                Console.Write($"{r} |");
                for (int c = 0; c < Cols; c++)
                {
                    int index = r * Cols + c;
                    if (revealed[index] || matched[index])
                    {
                        Console.Write($"{board[index]} ");
                    }
                    else
                    {
                        Console.Write("# "); // Hidden
                    }
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        public void Play()
        {
            int matchesFound = 0;
            int moves = 0;

            while (matchesFound < 8)
            {
                DrawBoard();

                // First pick
                int r1 = Program.GetIntInput("Pick first card Row (0-3): ", 0, 3);
                int c1 = Program.GetIntInput("Pick first card Column (0-3): ", 0, 3);
                int idx1 = r1 * Cols + c1;

                if (matched[idx1] || revealed[idx1])
                {
                    Console.WriteLine("Card already revealed! Try again.");
                    Thread.Sleep(1000);
                    continue;
                }

                revealed[idx1] = true;
                DrawBoard();

                // Second pick
                int r2 = Program.GetIntInput("Pick second card Row (0-3): ", 0, 3);
                int c2 = Program.GetIntInput("Pick second card Column (0-3): ", 0, 3);
                int idx2 = r2 * Cols + c2;

                if (idx1 == idx2 || matched[idx2])
                {
                    Console.WriteLine("Invalid selection! Try again.");
                    revealed[idx1] = false;
                    Thread.Sleep(1000);
                    continue;
                }

                revealed[idx2] = true;
                DrawBoard();
                moves++;

                // Check match
                if (board[idx1] == board[idx2])
                {
                    Console.WriteLine("Match found!");
                    matched[idx1] = true;
                    matched[idx2] = true;
                    matchesFound++;
                    Thread.Sleep(1000);
                }
                else
                {
                    Console.WriteLine("No match. Flipping back...");
                    Thread.Sleep(1500);
                    revealed[idx1] = false;
                    revealed[idx2] = false;
                }
            }

            Console.WriteLine($"Congratulations! You won in {moves} moves.");
            Console.WriteLine("Press Enter to return to menu...");
            Console.ReadLine();
        }
    }

    // ==========================================
    // GAME 2: CONNECT FOUR
    // ==========================================
    class ConnectFour
    {
        const int Rows = 6;
        const int Cols = 7;
        char[,] grid;

        public ConnectFour()
        {
            grid = new char[Rows, Cols];
            for (int r = 0; r < Rows; r++)
                for (int c = 0; c < Cols; c++)
                    grid[r, c] = '.';
        }

        void DrawBoard()
        {
            Console.Clear();
            Console.WriteLine("=== CONNECT FOUR ===");
            Console.WriteLine("Connect 4 to win (X or O).\n");

            for (int r = 0; r < Rows; r++)
            {
                Console.Write("|");
                for (int c = 0; c < Cols; c++)
                {
                    Console.Write($"{grid[r, c]} ");
                }
                Console.WriteLine("|");
            }
            Console.WriteLine("---------------");
            Console.WriteLine(" 0 1 2 3 4 5 6\n");
        }

        bool DropDisc(int col, char player)
        {
            if (grid[0, col] != '.') return false; // Column full

            for (int r = Rows - 1; r >= 0; r--)
            {
                if (grid[r, col] == '.')
                {
                    grid[r, col] = player;
                    return true;
                }
            }
            return false;
        }

        bool CheckWin(char p)
        {
            // Horizontal
            for (int r = 0; r < Rows; r++)
                for (int c = 0; c < Cols - 3; c++)
                    if (grid[r, c] == p && grid[r, c + 1] == p && grid[r, c + 2] == p && grid[r, c + 3] == p) return true;

            // Vertical
            for (int r = 0; r < Rows - 3; r++)
                for (int c = 0; c < Cols; c++)
                    if (grid[r, c] == p && grid[r + 1, c] == p && grid[r + 2, c] == p && grid[r + 3, c] == p) return true;

            // Diagonal /
            for (int r = 3; r < Rows; r++)
                for (int c = 0; c < Cols - 3; c++)
                    if (grid[r, c] == p && grid[r - 1, c + 1] == p && grid[r - 2, c + 2] == p && grid[r - 3, c + 3] == p) return true;

            // Diagonal \
            for (int r = 0; r < Rows - 3; r++)
                for (int c = 0; c < Cols - 3; c++)
                    if (grid[r, c] == p && grid[r + 1, c + 1] == p && grid[r + 2, c + 2] == p && grid[r + 3, c + 3] == p) return true;

            return false;
        }

        public void Play()
        {
            char currentPlayer = 'X';
            bool running = true;
            int turns = 0;

            while (running && turns < Rows * Cols)
            {
                DrawBoard();
                int col = Program.GetIntInput($"Player {currentPlayer}, choose column (0-6): ", 0, 6);

                if (DropDisc(col, currentPlayer))
                {
                    if (CheckWin(currentPlayer))
                    {
                        DrawBoard();
                        Console.WriteLine($"Player {currentPlayer} WINS!");
                        running = false;
                    }
                    else
                    {
                        currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
                        turns++;
                    }
                }
                else
                {
                    Console.WriteLine("Column full! Try again.");
                    Thread.Sleep(1000);
                }
            }

            if (turns == Rows * Cols && running)
            {
                DrawBoard();
                Console.WriteLine("It's a DRAW!");
            }

            Console.WriteLine("Press Enter to return to menu...");
            Console.ReadLine();
        }
    }

    // ==========================================
    // GAME 3: TIC-TAC-TOE
    // ==========================================
    class TicTacToe
    {
        char[,] board;

        public TicTacToe()
        {
            board = new char[3, 3];
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++)
                    board[i, j] = ' ';
        }

        void DrawBoard()
        {
            Console.Clear();
            Console.WriteLine("=== TIC-TAC-TOE ===\n");
            Console.WriteLine("  0   1   2");
            Console.WriteLine($"0 {board[0, 0]} | {board[0, 1]} | {board[0, 2]}");
            Console.WriteLine(" ---|---|---");
            Console.WriteLine($"1 {board[1, 0]} | {board[1, 1]} | {board[1, 2]}");
            Console.WriteLine(" ---|---|---");
            Console.WriteLine($"2 {board[2, 0]} | {board[2, 1]} | {board[2, 2]}\n");
        }

        bool CheckWin(char p)
        {
            for (int i = 0; i < 3; i++)
            {
                if (board[i, 0] == p && board[i, 1] == p && board[i, 2] == p) return true;
                if (board[0, i] == p && board[1, i] == p && board[2, i] == p) return true;
            }
            if (board[0, 0] == p && board[1, 1] == p && board[2, 2] == p) return true;
            if (board[0, 2] == p && board[1, 1] == p && board[2, 0] == p) return true;
            return false;
        }

        public void Play()
        {
            char currentPlayer = 'X';
            int moves = 0;
            bool won = false;

            while (moves < 9 && !won)
            {
                DrawBoard();
                Console.WriteLine($"Player {currentPlayer}'s turn.");
                int r = Program.GetIntInput("Row (0-2): ", 0, 2);
                int c = Program.GetIntInput("Col (0-2): ", 0, 2);

                if (board[r, c] == ' ')
                {
                    board[r, c] = currentPlayer;
                    won = CheckWin(currentPlayer);
                    if (!won) currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
                    moves++;
                }
                else
                {
                    Console.WriteLine("Space taken!");
                    Thread.Sleep(1000);
                }
            }

            DrawBoard();
            if (won) Console.WriteLine($"Player {currentPlayer} Wins!");
            else Console.WriteLine("It's a Draw!");

            Console.WriteLine("Press Enter to return to menu...");
            Console.ReadLine();
        }
    }
}