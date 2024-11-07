import os
from ui.map_menu import map_select_menu
from ui.simulate_game import simulate_single_game
from ui.pause_menu import choose_algorithm_menu
from ui.ui_utility import screen

# Define the output folder path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
output_folder = os.path.join(project_root, "output")

def start_game():
    selected_map_file, map_number = map_select_menu()

    if selected_map_file:
        # After selecting a map, allow the user to choose an algorithm
        chosen_algorithm = choose_algorithm_menu(screen, map_number)

        # Construct the output file path based on the chosen algorithm
        if chosen_algorithm:
            algorithm_output_folder = os.path.join(output_folder, chosen_algorithm)
            output_file = os.path.join(algorithm_output_folder, f"output-{map_number:02d}.txt")

            # Run the simulation for the selected map and algorithm
            simulate_single_game(selected_map_file, output_file, no_solution=False)