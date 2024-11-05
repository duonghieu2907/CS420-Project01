from UCS import *
from scipy.optimize import linear_sum_assignment

class CustomizeState (State):
    def __init__(self, ares_pos, stones, cost, path=""):
        super().__init__(ares_pos, stones, cost, path)
        self.heuristic = None
    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic
    def setHeuristic(self, value):
        self.heuristic = value

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star(weights, grid):
    initial_state = find_initial_state(grid)
    initial_state = CustomizeState(initial_state)
    initial_state.setHeuristic(heuristic_function(initial_state, weights, grid))
    initial_state.f_cost = initial_state.cost + initial_state.heuristic  # f_cost = g + h

    priority_queue = []
    heapq.heappush(priority_queue, (initial_state.f_cost, initial_state))
    visited = set()
    cost_dict = {initial_state: initial_state.f_cost}  # Track minimum f_cost for each state
    nodes_generated = 0

    start_time = time.time()
    tracemalloc.start()

    while priority_queue:
        _, current_state = heapq.heappop(priority_queue)
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
            successor.setHeuristic(heuristic_function(successor, weights, grid))
            successor.f_cost = successor.cost + successor.heuristic
            successor_key = (successor.ares_pos, tuple(successor.stones))

            # Check if the successor should be added or updated in the priority queue
            if successor_key not in visited or successor.f_cost < cost_dict.get(successor_key, float('inf')):
                cost_dict[successor_key] = successor.f_cost
                heapq.heappush(priority_queue, (successor.f_cost, successor))

    tracemalloc.stop()
    return None, nodes_generated, time.time() - start_time, 0


def heuristic_function(state, weights, grid):
    if goal_state(state, grid):
        return 0
    stones = state.stones  # Positions of stones (x1, x2, ..., xn)
    switches = [(i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if
                cell == '.']  # Positions of switches (y1, y2, ..., yn)
    ares_pos = state.ares_pos  # Position of Ares

    if len(stones) != len(switches):
        raise ValueError("The number of stones does not match the number of switches.")

    # Construct the cost matrix where cost[i][j] = Manhattan distance * weight of stone i to switch j
    cost_matrix = []
    for i, stone in enumerate(stones):
        row = []
        for switch in switches:
            distance = manhattan_distance(stone, switch)
            row.append(distance * weights[i])
        cost_matrix.append(row)

    # Solve the assignment problem to minimize the total weighted distance
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Calculate the total minimum weighted sum of stone-to-switch distances
    total_weighted_distance = sum(cost_matrix[i][j] for i, j in zip(row_ind, col_ind))

    # Additional cost: Sum of Manhattan distances from Ares to each stone
    ares_to_stones_distance = sum(manhattan_distance(ares_pos, stone) for stone in stones)

    # Combine the costs
    total_cost = total_weighted_distance + ares_to_stones_distance

    return total_cost


if __name__ == "__main__":
    input_folder = 'input'
    output_folder = 'output_A_Star'

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
                        write_output(output_path, "A Star Search", final_state, nodes_generated, time_taken,
                                     memory_used)
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
