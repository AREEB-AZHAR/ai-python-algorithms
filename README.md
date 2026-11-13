# 🧠 AI & Game Playing Algorithms in Python

A curated collection of artificial intelligence algorithms, adversarial game-playing engines, search heuristics, and computational decision-making implementations in Python 3.

---

## 🎮 Core Algorithms & Modules

### 1. Adversarial Search & Board Games
- **Alpha-Beta Pruning (`alphabeta.py`)**: Minimax search engine with alpha-beta pruning for zero-sum games, significantly cutting search complexity.
- **Checkers Engine (`checkers.py`)**: Full checkers game rules, state evaluation, and minimax-based AI decision logic.
- **Chess Engines (`chessGame.py`, `chessf.py`)**: Chess board representation, piece mobility validation, and move evaluation.
- **Connect 4 (`connect4.py`, `gamec4.py`)**: Vertical gravity grid board simulation, win-state detection, and heuristic AI play.
- **Tic-Tac-Toe (`tictac.py`)**: Unbeatable optimal game tree resolution using depth-limited Minimax.

### 2. Decision Support & Search Heuristics
- **Priority Heaps & Pathfinding (`heappp.py`, `short.py`)**: Binary heap implementations, priority queues, and shortest path search.
- **Gantt & Scheduling Engine (`ganttchart.py`, `Salary chart.py`)**: Algorithmic task scheduling and tabular visualization.
- **Data & Feature Engineering (`customer_data.csv`, `lab 10.py`, `lab13.py`)**: Statistical classification, dataset boundaries, and feature selection routines.

---

## 🚀 Getting Started

### Prerequisites
- **Python**: Version `3.10` or higher (compatible with Python 3.10 - 3.13)

### Installation & Run
No heavy external dependencies are required for core algorithms.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AREEB-AZHAR/ai-python-algorithms.git
   cd ai-python-algorithms
   ```

2. **Run an Adversarial AI Game**:
   ```bash
   # Play Checkers AI
   python checkers.py

   # Play Connect 4 AI
   python connect4.py

   # Run Alpha-Beta Pruning Evaluation
   python alphabeta.py
   ```

3. **Verify All Scripts**:
   You can verify the syntax and compilation of all scripts at once:
   ```bash
   python -m compileall .
   ```
