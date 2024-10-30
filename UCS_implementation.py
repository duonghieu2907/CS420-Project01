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

def goal_state(state, grid):
    for stone_pos in state.stones:
        x, y = stone_pos
        if grid[x][y] != '.':
            return False
    return True

def uniform_cost_search(weights, grid):
    initial_state = find_initial_state(grid)
    priority_queue = []
    heapq.heappush(priority_queue, initial_state)
    visited = set()
    nodes_generated = 0

    start_time = time.time()
    tracemalloc.start()

    while priority_queue:
        current_state = heapq.heappop(priority_queue)
        nodes_generated += 1

        if goal_state(current_state, grid):
            time_taken = time.time() - start_time
            memory_used = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            return current_state, nodes_generated, time_taken, memory_used

        state_key = (current_state.ares_pos, tuple(current_state.stones))
        if state_key in visited:
            continue
        visited.add(state_key)

        for successor in get_successors(current_state, weights, grid):
            successor_key = (successor.ares_pos, tuple(successor.stones))
            if successor_key not in visited:
                heapq.heappush(priority_queue, successor)

    tracemalloc.stop()
    return None, nodes_generated, time.time() - start_time, 0

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
        
if __name__ == "__main__":
    input_folder = 'input'
    output_folder = 'output_UCS'
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each input file
    for input_file in os.listdir(input_folder):
        input_path = os.path.join(input_folder, input_file)
        
        if os.path.isfile(input_path) and input_file.endswith(".txt"):
            try:

                weights, grid, error_message = parse_input(input_path)
                
                output_file = f"{os.path.splitext(input_file)[0]}.txt"

                output_path = os.path.join(output_folder, output_file)
                if error_message:
                    # Write error output if there was a parsing issue
                    try:
                        write_error_output(output_path, error_message)
                    except Exception as e:
                        print(f"Error writing error message to {output_path}: {e}")
                    continue
                
                final_state, nodes_generated, time_taken, memory_used = uniform_cost_search(weights, grid)
                
                
                
                 # Write output based on search result
                try:
                    if final_state:
                        write_output(output_path, "Uniform Cost Search", final_state, nodes_generated, time_taken, memory_used)
                    else:
                        with open(output_path, 'w') as f:
                            f.write("No solution found\n")
                except Exception as e:
                    print(f"Error writing output for {output_file}: {e}")
                        
                print(f"Processed {input_file} -> {output_file}")
            except FileNotFoundError:
                print(f"File not found: {input_path}")
            except IOError as e:
                print(f"I/O error with file {input_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing {input_file}: {e}")

