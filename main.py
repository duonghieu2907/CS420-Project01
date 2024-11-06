import os
from search_algorithms.UCS import UCS_process_input_files
from search_algorithms.BFS import BFS_process_input_files
from search_algorithms.DFS import DFS_process_input_files
from search_algorithms.A_star import A_star_process_input_files

if __name__ == "__main__":
    input_folder = 'input'
    output_folder = 'output'

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process input files with all search algorithms
    # ucs_results = UCS_process_input_files(input_folder)
    # bfs_results = BFS_process_input_files(input_folder)
    dfs_results = DFS_process_input_files(input_folder)
    # a_star_results = A_star_process_input_files(input_folder)

    for idx in range(len(dfs_results)):
        output_file = f"output-{idx + 1:02}.txt"
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'w') as f:
            for results in [dfs_results]:
                f.write(f"{results[idx]['algorithm']}\n")
                if results[idx]['error_message']:
                    f.write(f"{results[idx]['error_message']}\n\n")
                elif type(results[idx]['final_state']) == str:
                    f.write(results[idx]['final_state'] + "\n\n")
                else:
                    f.write(f"Steps: {len(results[idx]['final_state'].path)}\n")
                    f.write(f"Total Weight Pushed: {results[idx]['final_state'].cost - len(results[idx]['final_state'].path)}\n")
                    f.write(f"Nodes Generated: {results[idx]['nodes_generated']}\n")
                    f.write(f"Time Taken: {results[idx]['time_taken']:.4f} seconds\n")
                    f.write(f"Memory Used: {results[idx]['memory_used'] / 1024:.2f} KB\n")
                    f.write(results[idx]['final_state'].path + "\n\n")

