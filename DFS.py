from search_utility import *

def DFS_Search(weight: object, grid: object) -> object:
    initial_state = find_initial_state(grid)
    visited = set()
    nodes_generated = 0
    start_time = time.time()
    tracemalloc.start()
    search = recursive_dfs(initial_state, grid, tracemalloc, visited, start_time, nodes_generated)
    if search:
        return search
    else:
        print("No solution found.")
        return None, nodes_generated, time.time() - start_time, tracemalloc.get_traced_memory()[1]


def recursive_dfs(current_state, grid, tracemalloc, visited, start_time, nodes_generated):
    # Check if the current state is the goal state
    if goal_state(current_state, grid): #early check
        time_taken = time.time() - start_time
        memory_used = tracemalloc.get_traced_memory()[1]
        return current_state, nodes_generated, time_taken, memory_used

    # Increment nodes generated and create a unique key for the current state
    nodes_generated += 1
    state_key = (current_state.ares_pos, tuple(current_state.stones))

    # Skip states we've already visited
    if state_key in visited:
        return None
    visited.add(state_key)

    # Explore successors
    for successor in get_successors(current_state, weights, grid):
        result = recursive_dfs(successor, grid, tracemalloc, visited, start_time, nodes_generated)
        if result:
            return result  # Propagate the solution up if found

    # Return None if no solution is found along this path
    return None

if __name__ == "__main__":
    input_folder = 'input'
    output_folder = 'output_DFS'

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
                    try:
                        write_error_output(output_path, error_message)
                    except Exception as e:
                        print(f"Error writing error message to {output_path}: {e}")
                    continue

                final_state, nodes_generated, time_taken, memory_used = DFS_Search(weights, grid)

                try:
                    if final_state:
                        write_output(output_path, "Depth-First Search", final_state, nodes_generated, time_taken,
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