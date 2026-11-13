import heapq
import matplotlib.pyplot as plt
import numpy as np

# A* Algorithm Implementation
def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for row in range(rows) for node in [(row, col) for col in range(cols)]}
    g_score[start] = 0
    f_score = {node: float('inf') for row in range(rows) for node in [(row, col) for col in range(cols)]}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1] # Return reversed path

        # Neighbors: Up, Down, Left, Right
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check bounds and obstacles (1 is obstacle)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] == 0:
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

# Simulation Setup
# 0 = Path, 1 = Obstacle
grid = np.array([
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

start = (0, 0)
goal = (9, 9)

path = a_star_search(grid, start, goal)

# Visualization
if path:
    print(f"Path found! Length: {len(path)} steps.")
    x_coords = [p[1] for p in path]
    y_coords = [p[0] for p in path]
    
    plt.imshow(grid, cmap='Greys')
    plt.plot(x_coords, y_coords, color='red', linewidth=2, label='Optimal Path')
    plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
    plt.scatter(goal[1], goal[0], color='blue', marker='x', label='Goal')
    plt.legend()
    plt.title("OEL: Warehouse Robot Pathfinding (A*)")
    plt.show()
else:
    print("No path found.")