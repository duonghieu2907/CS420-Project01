import pygame
import sys
from ui_utility import *
from map_menu import *

# Position the buttons to be evenly spaced below the title
start_button = Button("Start Game", (WIDTH // 2, HEIGHT // 2))
credit_button = Button("Credit", (WIDTH // 2, HEIGHT // 2 + BUTTON_SPACING))
quit_button = Button("Quit", (WIDTH // 2, HEIGHT // 2 + 2 * BUTTON_SPACING))

# Main menu function
def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)

        # Draw title
        title_text = title_font.render("Sokoban", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        start_button.draw(screen, mouse_pos)
        credit_button.draw(screen, mouse_pos)
        quit_button.draw(screen, mouse_pos)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos):
                    map_select_menu()  # Opens the map selection menu
                elif credit_button.is_clicked(mouse_pos):
                    print("Credit clicked!")
                    # Insert credit logic here
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.flip()

# Run the menu
main_menu()
