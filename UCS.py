from search_utility import *

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