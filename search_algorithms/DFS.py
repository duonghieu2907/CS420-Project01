from typing import final
from .search_utility import *

OVER_RECURSION = -1
def DFS_Search(weights, grid) -> object:
    initial_state = find_initial_state(grid)
    visited = set()
    nodes_generated = 0
    start_time = time.time()
    tracemalloc.start()
    search = recursive_dfs(initial_state, grid, weights, tracemalloc, visited, start_time, nodes_generated)
    if search:
        return search
    else:
        print("No solution found.")
        return None, nodes_generated, time.time() - start_time, tracemalloc.get_traced_memory()[1]

def recursive_dfs(current_state, grid, weights, tracemalloc, visited, start_time, nodes_generated):
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
        try:
            result = recursive_dfs(successor, grid, weights, tracemalloc, visited, start_time, nodes_generated)
        except RecursionError:
            time_taken = time.time() - start_time
            memory_used = tracemalloc.get_traced_memory()[1]
            return OVER_RECURSION, nodes_generated, time_taken, memory_used

        if result:
            return result  # Propagate the solution up if found

    # Return None if no solution is found along this path
    return None

def DFS_process_input_files(input_folder: str) -> List[Dict[str, Any]]:
    output_data = []

    # Process each input file in the folder
    for input_file in os.listdir(input_folder):
        input_path = os.path.join(input_folder, input_file)
        
        if os.path.isfile(input_path) and input_file.endswith(".txt"):
            result = {
                "input_file": input_file,
                "algorithm": "Depth-First Search",
                "final_state": None,
                "nodes_generated": None,
                "time_taken": None,
                "memory_used": None,
                "error_message": None
            }

            try:
                # Parse input data
                weights, grid, error_message = parse_input(input_path)
                if error_message:
                    # If parsing error, save the error message in the result and skip the search
                    result["error_message"] = error_message
                    output_data.append(result)
                    continue
                
                # Run DFS on the parsed data
                final_state, nodes_generated, time_taken, memory_used = DFS_Search(weights, grid)
                
                # Store results
                result["final_state"] = final_state
                result["nodes_generated"] = nodes_generated
                result["time_taken"] = time_taken
                result["memory_used"] = memory_used
                
                # If no solution was found, mark it in the final_state
                if final_state == OVER_RECURSION:
                    result["final_state"] = "The searching got over the limit of recursion"
                elif not final_state:
                    result["final_state"] = "No solution found"


            except FileNotFoundError:
                result["error_message"] = f"File not found: {input_path}"
            except IOError as e:
                result["error_message"] = f"I/O error with file {input_path}: {e}"
            except Exception as e:
                result["error_message"] = f"An unexpected error occurred while processing {input_file}: {e}"

            # Append the result to the output data list
            output_data.append(result)

    return output_data