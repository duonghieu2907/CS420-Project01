import os
import heapq
import time
import tracemalloc
from typing import List, Tuple, Dict, Any

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
            # Parse weights, which should be on the first line
            weights = list(map(int, f.readline().strip().split()))
            
            # Parse the grid, keeping leading and trailing whitespace in each row
            grid = [list(line.rstrip('\n')) for line in f.readlines()]
        
        # Validate grid for the number of stones
        stone_count = sum(row.count('$') + row.count('*') for row in grid)
        if len(weights) != stone_count:
            error_message = f"Error: Number of stones does not match weights in {file}."
            return None, None, error_message
        
        return weights, grid, None
    
    except Exception as e:
        error_message = f"Error parsing file {file}: {e}"
        return None, None, error_message
    
def find_initial_state(grid) -> State:
    ares_pos = None
    stones = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                ares_pos = (i, j)
            elif cell == '$':
                stones.append((i, j))
            elif cell == '+':  # Player and Goal
                ares_pos = (i, j)
            elif cell == '*':  # Box and Goal
                stones.append((i, j))
    return State(ares_pos, stones, 0)

def is_valid_move(x, y, grid, stones):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] != '#' and (x, y) not in stones

def push_stone(ares_pos, stone_pos, grid, stones):
    x, y = stone_pos
    dx, dy = x - ares_pos[0], y - ares_pos[1]
    new_stone_pos = (x + dx, y + dy)
    if is_valid_move(new_stone_pos[0], new_stone_pos[1], grid, stones):
        return new_stone_pos
    return None

def goal_state(state, grid):
    for stone_pos in state.stones:
        x, y = stone_pos
        if grid[x][y] not in {'.', '+', '*'}:
            return False
    return True

def get_successors(state, weights, grid) -> List[State]:
    successors = []
    ares_x, ares_y = state.ares_pos
    directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]

    for dx, dy, move, push in directions:
        new_ares_pos = (ares_x + dx, ares_y + dy)

        if is_valid_move(new_ares_pos[0], new_ares_pos[1], grid, state.stones):
            successors.append(State(new_ares_pos, state.stones[:], state.cost + 1, state.path + move))

        for i, stone_pos in enumerate(state.stones):
            if stone_pos == new_ares_pos:
                new_stone_pos = push_stone(state.ares_pos, stone_pos, grid, state.stones)
                if new_stone_pos:
                    new_stones = state.stones[:]
                    new_stones[i] = new_stone_pos
                    stone_weight = weights[i]
                    successors.append(State(new_ares_pos, new_stones, state.cost + stone_weight + 1, state.path + push))

    return successors