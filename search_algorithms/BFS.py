from collections import deque
from .search_utility import *

def bfs_search(weights, grid):
    initial_state = find_initial_state(grid)
    queue = deque([initial_state])
    visited = set()
    nodes_generated = 0

    start_time = time.time()
    tracemalloc.start()

    while queue:
        current_state = queue.popleft()
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
                queue.append(successor)

    tracemalloc.stop()
    return None, nodes_generated, time.time() - start_time, 0

def BFS_process_input_files(input_folder: str) -> List[Dict[str, Any]]:
    output_data = []

    # Process each input file in the folder
    for input_file in os.listdir(input_folder):
        input_path = os.path.join(input_folder, input_file)
        
        if os.path.isfile(input_path) and input_file.endswith(".txt"):
            result = {
                "input_file": input_file,
                "algorithm": "Breadth-First Search",
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
                
                # Run BFS on the parsed data
                final_state, nodes_generated, time_taken, memory_used = bfs_search(weights, grid)
                
                # Store results
                result["final_state"] = final_state
                result["nodes_generated"] = nodes_generated
                result["time_taken"] = time_taken
                result["memory_used"] = memory_used
                
                # If no solution was found, mark it in the final_state
                if not final_state:
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
