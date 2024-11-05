import pygame
import sys
from ui_utility import *

# Algorithm selection menu with default background and map number display
def choose_algorithm_menu(screen, map_number):
    # Create buttons for algorithms
    algorithms = ["DFS", "BFS", "UCS", "A*"]
    algorithm_buttons = [Button(alg, (WIDTH // 2, HEIGHT // 2.25 + i * 75)) for i, alg in enumerate(algorithms)]
    
    # Font for displaying the map number
    title_text = title_font.render(f"Map {map_number}", True, TITLE_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5))

    while True:
        screen.fill(BACKGROUND_COLOR)  # Fill the screen with default background color

        # Display the map number at the top
        screen.blit(title_text, title_rect)

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw algorithm buttons
        for button in algorithm_buttons:
            button.draw(screen, mouse_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in algorithm_buttons:
                    if button.is_clicked(mouse_pos):
                        print(f"Algorithm {button.text} selected.")
                        return button.text  # Returns selected algorithm

        pygame.display.flip()
