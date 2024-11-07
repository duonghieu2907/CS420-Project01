import os
from search_algorithms.UCS import UCS_process_input_files
from search_algorithms.BFS import BFS_process_input_files
from search_algorithms.DFS import DFS_process_input_files
from search_algorithms.A_star import A_star_process_input_files

def write_results_to_folder(algorithm_name, results, output_folder):
    # Create the subfolder for the algorithm under the output folder
    algorithm_folder = os.path.join(output_folder, algorithm_name)
    os.makedirs(algorithm_folder, exist_ok=True)
    
    # Write results to the respective algorithm's folder
    for idx, result in enumerate(results):
        output_file = f"output-{idx + 1:02}.txt"
        output_path = os.path.join(algorithm_folder, output_file)
        with open(output_path, 'w') as f:
            f.write(f"{result['algorithm']}\n")
            if result['error_message']:
                f.write(f"{result['error_message']}\n\n")
            elif isinstance(result['final_state'], str):
                f.write(result['final_state'] + "\n\n")
            else:
                f.write(f"Steps: {len(result['final_state'].path)}\n")
                f.write(f"Total Weight Pushed: {result['final_state'].cost - len(result['final_state'].path)}\n")
                f.write(f"Nodes Generated: {result['nodes_generated']}\n")
                f.write(f"Time Taken: {result['time_taken']:.4f} seconds\n")
                f.write(f"Memory Used: {result['memory_used'] / 1024:.2f} KB\n")
                f.write(result['final_state'].path + "\n\n")

def process_all_algorithms(input_folder, output_folder):
    # Determine the input folder relative to the script's location
    script_dir = os.path.dirname(__file__)
    input_folder = os.path.join(script_dir, "input")

    # Process input files with each search algorithm and save to their respective subfolder
    ucs_results = UCS_process_input_files(input_folder)
    bfs_results = BFS_process_input_files(input_folder)
    dfs_results = DFS_process_input_files(input_folder)
    a_star_results = A_star_process_input_files(input_folder)

    # Write each algorithm's results to its own subfolder
    write_results_to_folder("UCS", ucs_results, output_folder)
    write_results_to_folder("BFS", bfs_results, output_folder)
    write_results_to_folder("DFS", dfs_results, output_folder)
    write_results_to_folder("A_star", a_star_results, output_folder)