def load_grid(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            grid.append([char for char in line.strip() if char != ' '])  # Convert each line into a list of characters
    return grid

grid = load_grid('input/input-01.txt')
for row in grid:
    print(row)

from collections import deque

# Directions for moving up, down, left, right
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Function to find Ares's position in the grid
def find_ares_position(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'A':  # Ares's starting point
                return (i, j)
    return None

# BFS function
def bfs(grid):

    # Find the starting position of Ares
    start = find_ares_position(grid)
    if start is None:
        print("Ares's starting position not found!")
        return

    n = len(grid)    # Rows
    m = len(grid[0]) # Columns
    
    # Find Ares' starting position (A)
    ares_position = start

    # Queue for BFS: (x, y, cost)
    queue = deque([(ares_position[0], ares_position[1], 0)])
    visited = set()
    visited.add((ares_position[0], ares_position[1]))
    
    while queue:
        x, y, cost = queue.popleft()
        
        # Check if we've reached the goal (all switches activated)
        # This check depends on how the goal state is defined in your problem

        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            
            # Check if the next position is within bounds and is not a wall or visited
            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] != '#' and (nx, ny) not in visited:
                # Add to queue if it's a valid move
                queue.append((nx, ny, cost + 1))
                visited.add((nx, ny))

    # Return result (for now just printing)
    return visited

visited_positions = bfs(grid)
print("Visited Positions:", visited_positions)
