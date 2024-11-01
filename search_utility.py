import os
import heapq
import time
import tracemalloc


class State:
    def __init__(self, ares_pos, stones, cost, path=""):
        self.ares_pos = ares_pos  # Position of Ares (x, y)
        self.stones = stones  # Position of all stones as a list of (x, y)
        self.cost = cost  # Accumulated cost to reach this state
        self.path = path  # Action path as a string

    def __lt__(self, other):
        return self.cost < other.cost
    
    
def parse_input(file):
    try:
        with open(file, 'r') as f:
            weights = list(map(int, f.readline().strip().split()))
            grid = [list(line.strip()) for line in f.readlines()]
        
        # Validate grid for number of stones
        stone_count = sum(row.count('$') for row in grid)
        if len(weights) != stone_count:
            error_message = f"Error: Number of stones does not match weights in {file}."
            return None, None, error_message
        
        return weights, grid, None
    
    except Exception as e:
        error_message = f"Error parsing file {file}: {e}"
        return None, None, error_message
    
    
def find_initial_state(grid):
    ares_pos = None
    stones = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                ares_pos = (i, j)
            elif cell == '$':
                stones.append((i, j))
    return State(ares_pos, stones, 0)


def is_valid_move(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] not in ['#', '$']


def push_stone(ares_pos, stone_pos, grid):
    x, y = stone_pos
    dx, dy = x - ares_pos[0], y - ares_pos[1]
    new_stone_pos = (x + dx, y + dy)
    if is_valid_move(new_stone_pos[0], new_stone_pos[1], grid):
        return new_stone_pos
    return None


def goal_state(state, grid):
    for stone_pos in state.stones:
        x, y = stone_pos
        if grid[x][y] != '.':
            return False
    return True


def get_successors(state, weights, grid):
    successors = []
    ares_x, ares_y = state.ares_pos
    directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

    for dx, dy, move, push in directions:
        new_ares_pos = (ares_x + dx, ares_y + dy)

        if is_valid_move(new_ares_pos[0], new_ares_pos[1], grid):
            successors.append(State(new_ares_pos, state.stones[:], state.cost + 1, state.path + move))

        for i, stone_pos in enumerate(state.stones):
            if stone_pos == new_ares_pos:
                new_stone_pos = push_stone(state.ares_pos, stone_pos, grid)
                if new_stone_pos:
                    new_stones = state.stones[:]
                    new_stones[i] = new_stone_pos
                    stone_weight = weights[i]
                    successors.append(State(new_ares_pos, new_stones, state.cost + stone_weight + 1, state.path + push))

    return successors


def write_output(file, algorithm_name, state, nodes_generated, time_taken, memory_used):
    with open(file, 'w') as f:
        f.write(f"{algorithm_name}\n")
        f.write(f"Steps: {len(state.path)}\n")
        f.write(f"Total Weight Pushed: {state.cost - len(state.path)}\n")
        f.write(f"Nodes Generated: {nodes_generated}\n")
        f.write(f"Time Taken: {time_taken:.4f} seconds\n")
        f.write(f"Memory Used: {memory_used / 1024:.2f} KB\n")
        f.write(state.path + "\n")


def write_error_output(file_path, error_message):
    with open(file_path, 'w') as f:
        f.write("Error\n")
        f.write(error_message + "\n")