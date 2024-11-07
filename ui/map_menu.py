import pygame
import sys
from ui_utility import *
from pause_menu import *

# List of maps
map_names = [f"Map {i+1}" for i in range(10)]
map_buttons = []

# Settings for grid and pagination
MAPS_PER_PAGE = 4
current_page = 0

# Generate map buttons for the current page
def create_map_buttons():
    map_buttons.clear()
    maps_on_page = map_names[current_page * MAPS_PER_PAGE:(current_page + 1) * MAPS_PER_PAGE]
    
    for i, map_name in enumerate(maps_on_page):
        row = i // 2  # Determine row (2 maps per row)
        col = i % 2   # Determine column
        x_position = WIDTH // 3 + col * 350
        y_position = HEIGHT // 3 + row * 210 + 40
        map_buttons.append(MapButton(map_name, (x_position, y_position)))

# Map selection menu function
def map_select_menu():
    global current_page
    create_map_buttons()
    
    # Create Back button at the top-left corner
    back_button = Button("Back", (60, 40))

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Draw title
        title_text = title_map_font.render("Select a Map", True, TITLE_TEXT_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        screen.blit(title_text, title_rect)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw map buttons
        for map_button in map_buttons:
            map_button.draw(screen, mouse_pos)
        
        # Draw Back button
        back_button.draw(screen, mouse_pos)

        # Draw left arrow if on a page after the first
        if current_page > 0:
            draw_arrow_button(screen, "left", (60, HEIGHT - 40), mouse_pos)

        # Draw right arrow if more pages are available
        if current_page < (len(map_names) - 1) // MAPS_PER_PAGE:
            draw_arrow_button(screen, "right", (WIDTH - 60, HEIGHT - 40), mouse_pos)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check Back button
                if back_button.is_clicked(mouse_pos):
                    return  # Exits map_select_menu and returns to main_menu
                
                # Check left arrow click
                if current_page > 0 and pygame.Rect(40, HEIGHT - 60, 40, 40).collidepoint(mouse_pos):
                    current_page -= 1
                    create_map_buttons()
                
                # Check right arrow click
                if current_page < (len(map_names) - 1) // MAPS_PER_PAGE and pygame.Rect(WIDTH - 80, HEIGHT - 60, 40, 40).collidepoint(mouse_pos):
                    current_page += 1
                    create_map_buttons()
                
                # Check map buttons
                for idx, map_button in enumerate(map_buttons):
                    actual_map_number = current_page * MAPS_PER_PAGE + idx + 1  # Calculate the correct map number
                    if map_button.is_clicked(mouse_pos):
                        selected_algorithm = choose_algorithm_menu(screen, actual_map_number)  # Pass the correct map number
                        if selected_algorithm:
                            print(f"{map_button.text} selected with {selected_algorithm} algorithm!")
                            # Insert logic to load the selected map with the chosen algorithm here

        # Update display
        pygame.display.flip()