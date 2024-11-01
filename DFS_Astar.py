import time
import tracemalloc
from heapq import heappop, heappush

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRECTION_NAMES = ['u', 'd', 'l', 'r']

# Manhattan distance in 2D
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Check if a position is within the grid bounds
def is_in_bounds(grid, pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

# Check if the position is not a wall
def is_walkable(grid, pos):
    x, y = pos
    return grid[x][y] in [" ", ".", "+"]

# Heuristic for A* (Manhattan Distance + Weight)
def heuristic(stones, switches, weights_list):
    return sum(weights_list[i] * min(manhattan_distance(stone, switch) for switch in switches) for i, stone in enumerate(stones))

# Parse input grid to extract start position, stones, switches, and walls
def parse_grid(grid, weights_list):
    start = None
    stones = []
    switches = []
    weights = {}

    stone_index = 0  # To track which stone we are assigning weight to
    
    for i in range(len(grid)):
        for j in range(len(grid[0])): 
            if grid[i][j] == '@' or grid[i][j] == '+':  # Ares' starting position
                start = (i, j)
            elif grid[i][j] == '$' or grid[i][j] == '*':  # Stone position
                stones.append((i, j))
                weights[(i, j)] = weights_list[stone_index]  # Assign weight from weights_list
                stone_index += 1
            elif grid[i][j] == '.':  # Switch position
                switches.append((i, j))

    return start, stones, switches, weights

# Track memory and time
def track_resources(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        memory_usage, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if result != -1:
            result['time'] = (end_time - start_time) * 1000  # Convert to ms
            result['memory'] = memory_usage / (1024 * 1024)  # Convert to MB
        return result
    return wrapper

@track_resources
def dfs(grid, weights_list):
    start, stones, switches, weights = parse_grid(grid, weights_list)
    stack = [(start, stones, 0, [])]  # (current_position, stones_positions, cost, path)
    visited = set()
    nodes_generated = 0
    total_weight = 0
    
    while stack:
        position, current_stones, cost, path = stack.pop()
        nodes_generated += 1
        
        # Visited check includes both Ares' position and stones' positions
        state = (position, tuple(current_stones))
        if state in visited:
            continue
        
        visited.add(state)
        
        # Check if all stones are on switches
        if all(stone in switches for stone in current_stones):
            return {'steps': len(path), 'weight': total_weight, 'nodes': nodes_generated, 'path': ''.join(path)}
        
        for direction, (dx, dy) in enumerate(DIRECTIONS):
            new_position = (position[0] + dx, position[1] + dy)
            
            # Move without pushing
            if is_in_bounds(grid, new_position) and is_walkable(grid, new_position):
                stack.append((new_position, current_stones, cost + 1, path + [DIRECTION_NAMES[direction]]))
            
            # Check if there's a stone we can push
            if new_position in current_stones:
                stone_index = current_stones.index(new_position)
                next_position = (new_position[0] + dx, new_position[1] + dy)
                
                # Check if the space behind the stone is valid for a push
                if is_in_bounds(grid, next_position) and is_walkable(grid, next_position) and next_position not in current_stones:
                    # Push the stone
                    new_stones = list(current_stones)
                    new_stones[stone_index] = next_position
                    total_weight += weights_list[stone_index]  # Use the index to retrieve the stone's weight
                    stack.append((new_position, new_stones, cost + 1 + weights_list[stone_index], path + [DIRECTION_NAMES[direction].upper()]))
    
    return {'steps': 0, 'weight': 0, 'nodes': nodes_generated, 'path': ''}

@track_resources
def a_star(grid, weights_list):
    start, stones, switches, weights = parse_grid(grid, weights_list)
    heap = [(heuristic(stones, switches, weights_list), 0, start, stones, [])]  # (f, cost, position, stones, path)
    visited = set()
    nodes_generated = 0
    total_weight = 0
    
    while heap:
        f, cost, position, current_stones, path = heappop(heap)
        nodes_generated += 1
        
        # Visited check includes both Ares' position and stones' positions
        state = (position, tuple(current_stones))
        if state in visited:
            continue
        
        visited.add(state)
        
        # Check if all stones are on switches
        if all(stone in switches for stone in current_stones):
            return {'steps': len(path), 'weight': total_weight, 'nodes': nodes_generated, 'path': ''.join(path)}
        
        for direction, (dx, dy) in enumerate(DIRECTIONS):
            new_position = (position[0] + dx, position[1] + dy)
            
            # Move without pushing
            if is_in_bounds(grid, new_position) and is_walkable(grid, new_position):
                heappush(heap, (cost + 1 + heuristic(current_stones, switches, weights_list), cost + 1, new_position, current_stones, path + [DIRECTION_NAMES[direction]]))
            
            # Check if there's a stone we can push
            if new_position in current_stones:
                stone_index = current_stones.index(new_position)
                next_position = (new_position[0] + dx, new_position[1] + dy)
                
                # Check if the space behind the stone is valid for a push
                if is_in_bounds(grid, next_position) and is_walkable(grid, next_position) and next_position not in current_stones:
                    # Push the stone
                    new_stones = list(current_stones)
                    new_stones[stone_index] = next_position
                    total_weight += weights_list[stone_index]  # Use the index to retrieve the stone's weight
                    new_cost = cost + 1 + weights_list[stone_index]
                    heappush(heap, (new_cost + heuristic(new_stones, switches, weights_list), new_cost, new_position, new_stones, path + [DIRECTION_NAMES[direction].upper()]))
    
    return {'steps': 0, 'weight': 0, 'nodes': nodes_generated, 'path': ''}

# Read input
def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    weights_list = list(map(int, lines[0].strip().split()))
    grid = [list(line.strip()) for line in lines[1:]]
    
    return grid, weights_list

# Output to a text file
def write_output_file(filename, algorithm_name, result):
    with open(filename, 'w') as file:
        file.write(f"{algorithm_name}\n")
        file.write(f"Steps: {result['steps']}, Weight: {result['weight']}, Nodes: {result['nodes']}, Time (ms): {result['time']:.2f}, Memory (MB): {result['memory']:.2f}\n")
        file.write(f"{result['path']}\n")

# Test with input-01
grid_01, weights_list_01 = read_input_file('input-01.txt')

dfs_result_01 = dfs(grid_01, weights_list_01)
write_output_file('output-01.txt', 'DFS', dfs_result_01)

astar_result_01 = a_star(grid_01, weights_list_01)
write_output_file('output-02.txt', 'A*', astar_result_01)

# Test with input-02
grid_02, weights_list_02 = read_input_file('input-02.txt')

dfs_result_02 = dfs(grid_02, weights_list_02)
write_output_file('output-03.txt', 'DFS', dfs_result_02)

astar_result_02 = a_star(grid_02, weights_list_02)
write_output_file('output-04.txt', 'A*', astar_result_02)