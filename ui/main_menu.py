import pygame
import os
import sys
from .ui_utility import *
from .pause_menu import choose_algorithm_menu
from .simulate_game import simulate_single_game

# Project root and folders for input/output
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
input_folder = os.path.join(project_root, "input")
output_folder = os.path.join(project_root, "output")

# Initialize list of maps and pagination settings
map_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])
current_map_idx = 0

# Function to load the map and weights from the input file
def load_map_with_weights(file_path):
    with open(file_path, 'r') as f:
        # Read weights from the first line
        weights = list(map(int, f.readline().strip().split()))
        
        # Read the grid layout
        grid = [list(line.rstrip('\n')) for line in f.readlines()]
    return grid, weights

# Function to render map with optional page and additional instructions text
def render_map(grid, weights, page_text, additional_text=""):
    screen.fill(BACKGROUND_COLOR)
    
    # Render page indicator
    page_text_rendered = FONT.render(page_text, True, (0, 0, 0))
    screen.blit(page_text_rendered, (WIDTH // 2 - page_text_rendered.get_width() // 2, 10))

    # Counter for weights (to display each weight above the respective stone)
    weight_index = 0

    # Render grid
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
            screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))
            
            # If the cell is a stone or a stone in the basket (marked by $ or *), display the corresponding weight above it
            if (cell == '$' or cell == '*') and weight_index < len(weights):
                weight_text = FONT.render(str(weights[weight_index]), True, (255, 255, 255))
                screen.blit(weight_text, (x + SQUARE_SIZE // 4, y - 5))  # Display weight above the yarn
                weight_index += 1

    # Render navigation instructions
    instructions = FONT.render("Use LEFT and RIGHT arrows to navigate maps.", True, (0, 0, 0))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT + HEADER_HEIGHT + 10))

    # Render additional text, if provided
    if additional_text:
        additional_text_rendered = FONT.render(additional_text, True, (0, 0, 0))
        screen.blit(additional_text_rendered, (WIDTH // 2 - additional_text_rendered.get_width() // 2, HEIGHT + HEADER_HEIGHT - 40))

# Function to render the map display with navigation arrows and click-to-select
def map_selection_screen():
    global current_map_idx
    running = True

    # Main loop for map selection screen
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Load and display the current map along with stone weights
        map_file = os.path.join(input_folder, map_files[current_map_idx])
        grid, weights = load_map_with_weights(map_file)  # Load map and weights
        map_number = current_map_idx + 1
        page_text = f"Map {map_number} of {len(map_files)}"

        # Render map centered on the screen with weights displayed above stones
        render_map(grid, weights, page_text, additional_text="Click to select this map")

        # Draw navigation arrows for previous and next maps
        mouse_pos = pygame.mouse.get_pos()
        if current_map_idx > 0:
            draw_arrow_button(screen, "left", (60, HEIGHT - 40), mouse_pos)
        if current_map_idx < len(map_files) - 1:
            draw_arrow_button(screen, "right", (WIDTH - 60, HEIGHT - 40), mouse_pos)

        # Create a back button
        back_button = Button("Back", (30, 20), font = small_font)
        back_button.draw(screen, mouse_pos)

        # Event handling for navigation and map selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the back button is clicked
                if back_button.is_clicked(event.pos):
                    running = False  # Exit the map selection screen and return to main menu
                # Navigate to previous map
                elif current_map_idx > 0 and pygame.Rect(40, HEIGHT - 60, 40, 40).collidepoint(mouse_pos):
                    current_map_idx -= 1
                # Navigate to next map
                elif current_map_idx < len(map_files) - 1 and pygame.Rect(WIDTH - 80, HEIGHT - 60, 40, 40).collidepoint(mouse_pos):
                    current_map_idx += 1
                # Select the current map and go to algorithm choice
                else:
                    # Algorithm selection for the chosen map
                    chosen_algorithm = choose_algorithm_menu(screen, map_number)
                    if chosen_algorithm:
                        # Define output file path based on chosen algorithm
                        algorithm_output_folder = os.path.join(output_folder, chosen_algorithm.replace("*", "_star"))
                        output_file = os.path.join(algorithm_output_folder, f"output-{map_number:02d}.txt")
                        print(f"Map {map_number} selected with {chosen_algorithm} algorithm!")

                        # Run the simulation for the selected map and algorithm
                        simulate_single_game(map_file, output_file, weights)

        pygame.display.flip()

# Function to show credits
def show_credits():
    running = True
    title_font = pygame.font.Font(None, 60)
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Display credit text
        credit_text = title_font.render("Game developed by Team Knitting Kitten", True, TITLE_COLOR)
        credit_rect = credit_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(credit_text, credit_rect)

        # Display team member names
        names = [
            "Duong Trung Hieu",
            "Duong Ngoc Quang Khiem",
            "Cao Vo Nhat Minh",
            "Tran Nhat Thanh"
        ]
        for index, name in enumerate(names):
            name_text = FONT.render(name, True, TITLE_COLOR)
            name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + (index + 2) * 30))  # Spacing names
            screen.blit(name_text, name_rect)

        # Create a back button
        back_button = Button("Back", (30, 20), font = small_font)
        back_button.draw(screen, pygame.mouse.get_pos())

        # Event handling for quitting the credits screen or going back
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    running = False  # Exit credits screen when back button is clicked

        pygame.display.flip()

# Function to initialize Pygame and open the main menu
def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)

        # Draw title and buttons for main menu
        title_text = title_font.render("Knitting Kitten", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Get mouse position and button instances
        mouse_pos = pygame.mouse.get_pos()
        start_button = Button("Start Game", (WIDTH // 2, HEIGHT // 2))
        credit_button = Button("Credit", (WIDTH // 2, HEIGHT // 2 + BUTTON_SPACING))
        quit_button = Button("Quit", (WIDTH // 2, HEIGHT // 2 + 2 * BUTTON_SPACING))

        # Draw buttons
        start_button.draw(screen, mouse_pos)
        credit_button.draw(screen, mouse_pos)
        quit_button.draw(screen, mouse_pos)

        # Event handling for main menu buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos):
                    map_selection_screen()  # Start the map selection screen
                elif credit_button.is_clicked(mouse_pos):
                    show_credits() 
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()