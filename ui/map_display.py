import pygame
import os
from ui_utility import screen, IMAGES, FONT, SQUARE_SIZE, BACKGROUND_COLOR, WIDTH, HEIGHT, HEADER_HEIGHT, FOOTER_HEIGHT, load_map

# Function to render map
def render_map(grid, page_text):
    screen.fill(BACKGROUND_COLOR)
    
    page_text_rendered = FONT.render(page_text, True, (0, 0, 0))
    screen.blit(page_text_rendered, (WIDTH // 2 - page_text_rendered.get_width() // 2, 10))

    # Render the grid below the header
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            x, y = j * SQUARE_SIZE, HEADER_HEIGHT + i * SQUARE_SIZE
            screen.blit(IMAGES.get(cell, IMAGES[" "]), (x, y))

    instructions = FONT.render("Use LEFT and RIGHT arrow keys to navigate maps.", True, (0, 0, 0))
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT + HEADER_HEIGHT + 10))

# Main loop for displaying maps
def map_display():
    input_folder = "input"
    map_files = sorted([f for f in os.listdir(input_folder) if f.endswith(".txt")])

    if not map_files:
        print("No map files found in the input folder.")
        pygame.quit()
        return

    # Start with the first map
    current_map_idx = 0
    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))

    while True:
        # Determine page indicator text
        page_text = f"Map {current_map_idx + 1} {'(end)' if current_map_idx == len(map_files) - 1 else ''}"

        # Render the map and footer text
        render_map(grid, page_text)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and current_map_idx < len(map_files) - 1:
                    current_map_idx += 1
                    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))
                elif event.key == pygame.K_LEFT and current_map_idx > 0:
                    current_map_idx -= 1
                    grid = load_map(os.path.join(input_folder, map_files[current_map_idx]))

        pygame.display.flip()

# Test
map_display()