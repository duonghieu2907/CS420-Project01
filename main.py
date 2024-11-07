import pygame
import os
from ui.ui_utility import *
from ui.main_menu import main_menu
from process_algorithms import process_all_algorithms

# Navigate to the project root and ensure input/output folders are set up
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
input_folder = os.path.join(project_root, "input")
output_folder = os.path.join(project_root, "output")

def main():
    # Initialize Pygame and open the main menu
    pygame.init()
    # process_all_algorithms(input_folder, output_folder)
    main_menu()

if __name__ == "__main__":
    main()