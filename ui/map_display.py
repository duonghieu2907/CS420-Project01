import pygame
import os

pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 600
HEADER_HEIGHT = 50  # Reserved at the top for the header
FOOTER_HEIGHT = 50  # Reserved at the bottom for instructions
screen = pygame.display.set_mode((WIDTH, HEIGHT + HEADER_HEIGHT + FOOTER_HEIGHT))  # Adjust window height
pygame.display.set_caption("Map Display")

# Load images for symbols 
IMAGES = {
    "#": pygame.image.load("items/wall.png"),
    " ": pygame.image.load("items/floor.png"),
    "$": pygame.image.load("items/knitting_ball.png"),
    ".": pygame.image.load("items/basket.png"),
    "*": pygame.image.load("items/ball_in_basket.png"),
    "+": pygame.image.load("items/cat_in_basket.png"),
    "@": pygame.image.load("items/cat.png"),
}

# Set square size and font
SQUARE_SIZE = 60  # Max size of each tile
FONT = pygame.font.Font(None, 36)

# Function to render the map
def render_map(grid, page_text):
    screen.fill((253, 240, 213))  # Background color
    
    # Render page indicator in the header area
    page_text_rendered = FONT.render(page_text, True, (0, 0, 0))
    screen.blit(page_text_rendered, (WIDTH // 2 - page_text_rendered.get_width() // 2, 10))

    # Render the grid below the header
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE  # Offset y by HEADER_HEIGHT
            screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    # Render navigation instructions in the footer area
    instructions = FONT.render("Use LEFT and RIGHT arrow keys to navigate maps.", True, (0, 0, 0))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT + HEADER_HEIGHT + 10))

# Function to load map from file
def load_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    grid = [list(line.strip()) for line in lines[1:]]  # Skipping weights on first line if present
    return grid

# Main loop for displaying maps
def map_display():
    input_folder = "input"
    map_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])

    # Ensure there are map files to display
    if not map_files:
        print("No map files found in the input folder.")
        pygame.quit()
        return

    # Start with the first map
    current_map_idx = 0
    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))

    while True:
        # Determine page indicator text
        if current_map_idx  == len(map_files) - 1:
            page_text = f"Map {current_map_idx + 1} (end)"
        else:
            page_text = f"Map {current_map_idx + 1}"

        # Render the map and footer text
        render_map(grid, page_text)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                # Navigate to the next map with the right arrow key
                if event.key == pygame.K_RIGHT and current_map_idx < len(map_files) - 1:
                    current_map_idx += 1
                    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))
                # Navigate to the previous map with the left arrow key
                elif event.key == pygame.K_LEFT and current_map_idx > 0:
                    current_map_idx -= 1
                    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))

        # Update the display
        pygame.display.flip()

# Run map display
map_display()